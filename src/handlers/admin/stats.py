from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from asyncpg.pool import Pool

import keyboards.admin as admin_keyboards
import config as cfg

from filters import IsAdmin
from db.crud import UserDB, ApplicationDB

router=Router()


@router.message(IsAdmin(), Command('admin'))
async def admin(message: Message, state: FSMContext):
    await state.clear()
    
    await message.answer(
        text='👨‍💼 <strong>Вы в административной панели!</strong>\n<i>Здесь вы можете управлять ботом и просматривать статистику.</i>',
        reply_markup=admin_keyboards.main_menu_admin(),
        parse_mode='HTML'
    )
    
    
@router.callback_query(IsAdmin(), F.data == 'main_menu_admin')
async def main_menu_admin(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    
    await callback.answer()
    try:
        await callback.message.edit_text(
            text='👨‍💼 <strong>Вы в административной панели!</strong>\n<i>Здесь вы можете управлять ботом и просматривать статистику.</i>',
            reply_markup=admin_keyboards.main_menu_admin(),
            parse_mode='HTML'
        )
    except:
        await callback.message.delete()
        await callback.message.answer(
            text='👨‍💼 <strong>Вы в административной панели!</strong>\n<i>Здесь вы можете управлять ботом и просматривать статистику.</i>',
            reply_markup=admin_keyboards.main_menu_admin(),
            parse_mode='HTML'
        )
    

@router.callback_query(IsAdmin(), F.data == 'users_stats')
async def users_stats(callback: CallbackQuery, pool: Pool):
    user_db = UserDB(pool)
    
    await callback.answer()
    page=1
    total_users = await user_db.get_users_count()
    total_pages = (total_users + cfg.USERS_PER_PAGE - 1) // cfg.USERS_PER_PAGE
    users = await user_db.get_users_list(offset=(page-1)*cfg.USERS_PER_PAGE)
    await callback.message.edit_text(
        text='📊 <strong>Статистика пользователей:</strong>\n<i>Здесь будет отображаться количество зарегистрированных пользователей.</i>',
        reply_markup=admin_keyboards.make_user_keyboard(page, users, total_pages),
        parse_mode='HTML'
    )
    

@router.callback_query(F.data.startswith("page:"))
async def change_page(callback: CallbackQuery, pool: Pool):
    user_db = UserDB(pool)
        
    page = int(callback.data.split(":")[1])
    total_users = await user_db.get_users_count()
    total_pages = (total_users + cfg.USERS_PER_PAGE - 1) // cfg.USERS_PER_PAGE
    users = await user_db.get_users_list(offset=(page-1)*cfg.USERS_PER_PAGE)
    keyboard = admin_keyboards.make_user_keyboard(page, users, total_pages)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    

@router.callback_query(F.data.startswith("user:"))
async def show_user(callback: CallbackQuery, pool: Pool):
    user_db = UserDB(pool)
    
    tg_id = int(callback.data.split(":")[1])
    user = await user_db.get_user(user_id=tg_id)
    if user:
        text = (
            f"ID: {user['id']}\n"
            f"Telegram ID: {user['tg_id']}\n"
            f"Username: {user['username']}\n"
            f"ФИО: {user['full_name']}\n"
            f"Дата рождения: {user['date_birth']}\n"
            f"Номер: {user['number']}"
        )
        await callback.message.edit_text(
            text=text,
            reply_markup=admin_keyboards.back_to_list_users(),
            parse_mode='HTML'
        )
    else:
        await callback.message.answer("Пользователь не найден")
        
        
@router.callback_query(F.data == "applications_stats")
async def applications_stats(callback: CallbackQuery, pool: Pool):
    application_db = ApplicationDB(pool)
    
    await callback.answer()
    page=1
    total_applications = await application_db.get_applications_count()
    total_pages = (total_applications + cfg.APPLICATIONS_PER_PAGE - 1) // cfg.APPLICATIONS_PER_PAGE
    applications = await application_db.get_applications_list(offset=(page-1)*cfg.APPLICATIONS_PER_PAGE)
    try:
        await callback.message.edit_text(
            text='📊 <strong>Статистика заявок:</strong>\n<i>Здесь будет отображаться количество заявок и их статус.</i>',
            reply_markup=admin_keyboards.make_application_keyboard(page, applications, total_pages),
            parse_mode='HTML'
        )
    except:
        await callback.message.delete()
        await callback.message.answer(
            text='📊 <strong>Статистика заявок:</strong>\n<i>Здесь будет отображаться количество заявок и их статус.</i>',
            reply_markup=admin_keyboards.make_application_keyboard(page, applications, total_pages),
            parse_mode='HTML'
        )
    

@router.callback_query(F.data.startswith("aplication_page:"))
async def change_page(callback: CallbackQuery, pool: Pool):
    application_db = ApplicationDB(pool)
    
    page = int(callback.data.split(":")[1])
    total_applications = await application_db.get_applications_count()
    total_pages = (total_applications + cfg.APPLICATIONS_PER_PAGE - 1) // cfg.APPLICATIONS_PER_PAGE
    applications = await application_db.get_applications_list(offset=(page-1)*cfg.APPLICATIONS_PER_PAGE)
    keyboard = admin_keyboards.make_application_keyboard(page, applications, total_pages)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    
    
@router.callback_query(F.data.startswith("application:"))
async def show_application(callback: CallbackQuery, pool: Pool):
    user_db = UserDB(pool)
    application_db = ApplicationDB(pool)
    
    await callback.answer()
    
    application_id = int(callback.data.split(":")[1])
    application = await application_db.get_application_by_id(application_id=application_id)
    if application:
        user = await user_db.get_user(user_id=application['user_id'])
        text = (
            f"ID: {application['id']}\n"
            f"Клиент: {user['full_name']}\n"
            f"Телефон: {user['number']}\n"
            f"Услуга: {application['service']}\n"
            f"Технологии: {application['technologies']}\n"
            f"Срок выполнения: {application['deadline']}\n"
            f"Описание: {application['description']}"
        )
        if application['screenshot']:
            await callback.message.delete()
            await callback.message.answer_photo(
                photo=application['screenshot'],
                caption=text,
                reply_markup=admin_keyboards.back_to_list_applications(),
                parse_mode='HTML'
            )
        else:
            await callback.message.edit_text(
                text=text,
                reply_markup=admin_keyboards.back_to_list_applications(),
                parse_mode='HTML'
            )
    else:
        await callback.message.answer("Заявка не найдена")
        
        
@router.callback_query(F.data == "all_stats")
async def all_stats(callback: CallbackQuery, pool: Pool):
    user_db = UserDB(pool)
    application_db = ApplicationDB(pool)
    
    await callback.answer()
    total_users = await user_db.get_users_count()
    total_applications = await application_db.get_applications_count()
    
    text = (
        f"📊 <strong>Общая статистика:</strong>\n"
        f"👥 <strong>Пользователей:</strong> {total_users}\n"
        f"📝 <strong>Заявок:</strong> {total_applications}"
    )
    
    await callback.message.edit_text(
        text=text,
        reply_markup=admin_keyboards.back_to_main_menu(),
        parse_mode='HTML'
    )
