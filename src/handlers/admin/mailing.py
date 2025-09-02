import asyncio

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from asyncpg.pool import Pool

import keyboards.admin as admin_keyboards

from states import UserMailing
from db.crud import UserDB
from utils.admin import delete_message_with_timeout


router = Router()


@router.callback_query(F.data == 'mailing')
async def mailing(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        text='📬 <strong>Рассылка сообщений</strong>\n<i>Здесь вы можете отправить сообщение всем пользователям бота.</i>\nК сообщению можно прикрепить <strong>одно</strong> фото',
        reply_markup=admin_keyboards.back_to_main_menu(),
        parse_mode='HTML'
    )
    await state.set_state(UserMailing.message)
    

@router.message(UserMailing.message)
async def get_mailing_message(message: Message, state: FSMContext):
    await message.bot.edit_message_reply_markup(
        chat_id=message.chat.id,
        message_id=message.message_id - 1,
        reply_markup=None
    )
    
    text = message.html_text.strip()
    file_id = message.photo[-1].file_id if message.photo else None
    
    await state.update_data(message=text, photo=file_id)
    await state.set_state(None)
    
    await message.answer(
        text='📬 <strong>Отлично, теперь выбери выберите время отправки рекламы:</strong>',
        reply_markup=admin_keyboards.mailing_time(),
        parse_mode='HTML'
    )
    

@router.callback_query(F.data.startswith('view_set_timer:'))
async def set_mailing_timer(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    timer = int(callback.data.split(':')[1])
    await state.update_data(timer=timer)
    
    await callback.message.edit_text(
        text='<b>Выберите период времени в часах, по прошествии которого необходимо автоматически удалить рекламу.</b>',
        reply_markup=admin_keyboards.mailing_delete_time(),
        parse_mode='HTML'
    )
    

@router.callback_query(F.data.startswith('view_set_delete_timer:'))
async def set_mailing_delete_time(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    delete_time = int(callback.data.split(':')[1])
    await state.update_data(delete_time=delete_time)
    
    data = await state.get_data()
    message_text = data.get('message')
    photo_id = data.get('photo')
    timer = data.get('timer')
    
    text = (
        f'Вы собираетесь отправить следующее сообщение:\n\n'
        f'<strong>Сообщение:</strong> {message_text}\n'
        f'<strong>Тайминг отправки:</strong> {timer} секунд\n'
        f'<strong>Тайминг удаления:</strong> {delete_time} секунд\n'
    )
    
    if photo_id:
        await callback.message.delete()
        await callback.message.answer_photo(
            photo=photo_id,
            caption=text,
            reply_markup=admin_keyboards.confirm_mailing(),
            parse_mode='HTML'
        )
    else:
        await callback.message.edit_text(
            text=text,
            reply_markup=admin_keyboards.confirm_mailing(),
            parse_mode='HTML'
        )
        
        
@router.callback_query(F.data == 'confirm_mailing')
async def confirm_mailing(callback: CallbackQuery, state: FSMContext, pool: Pool):
    user_db = UserDB(pool)
    
    await callback.answer('Рассылка началась! Ожидайте')
    
    data = await state.get_data()
    message_text = data.get('message')
    photo_id = data.get('photo')
    timer = data.get('timer')
    delete_time = data.get('delete_time')
    
    await asyncio.sleep(int(timer))
    
    users = await user_db.get_all_users()
    count = 0
    for user in users:
        user_id = user['tg_id']
        try:
            if photo_id:
                msg = await callback.message.bot.send_photo(
                    chat_id=user_id,
                    photo=photo_id,
                    caption=message_text,
                    parse_mode='HTML'
                )
            else:
                msg = await callback.message.bot.send_message(
                    chat_id=user_id,
                    text=message_text,
                    parse_mode='HTML'
                )
            count+=1
            if delete_time > 0:
                await delete_message_with_timeout(delete_time, msg)
        except Exception as e:
            print(f"Error sending message to {user_id}: {e}")
            
            
    await callback.message.answer(
        text=f'✅ <strong>Рассылка завершена!</strong>\n<i>Сообщение было отправлено <strong>{count}</strong> пользователям.</i>',
        reply_markup=admin_keyboards.back_to_main_menu(),
        parse_mode='HTML'
    )
    await state.clear()
