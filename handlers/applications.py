import os

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext


import keyboards.user as user_keyboards

from states import UserApplications
from keyboards.user import TECHS
from db.requests import add_application, get_last_application_by_user, get_user


router = Router()


user_choices = {}


@router.message(F.text == '📝 Оставить заявку')
async def leave_request(message: Message, state: FSMContext):
    await message.answer(
        text='<strong>Хорошо!</strong> Давай начнем с того, какую услугу ты хочешь заказать? 🛠️\n<i>Выбери услугу, которую ты хочешь получить:</i>',
        reply_markup=await user_keyboards.application_services(),
        parse_mode='HTML'
    )
    await state.set_state(UserApplications.service)


@router.message(UserApplications.service)
async def get_service(message: Message, state: FSMContext):
    service = message.text.strip()

    if service == 'Назад':
        await message.answer(
            text='<strong>✅ Вы вернулись в главное меню.</strong>',
            reply_markup=await user_keyboards.main_menu(),
            parse_mode='HTML'
        )
        await state.clear()
        return

    if service not in ['Разработка сайта', 'Мобильное приложение', 'Техническая поддержка', 'Консультация']:
        await message.answer(
            text='❌ <strong>Пожалуйста, выбери услугу из предложенных вариантов</strong>',
            parse_mode='HTML'
        )
        return

    await state.update_data(service=service)
    await message.answer(
        text='<strong>Отлично!</strong> Теперь опиши свою заявку подробнее. 📝\n<i>Напиши описание услуги, которую ты хочешь заказать.</i>\n<i>Можно прикрепить скриншот, чтобы было понятнее.</i>',
        reply_markup=await user_keyboards.miss(),
        parse_mode='HTML'
    )
    await state.set_state(UserApplications.description)


@router.message(UserApplications.description)
async def get_description(message: Message, state: FSMContext):
    description = message.text.strip() if message.text else message.caption if message.caption else None
    file_id = message.photo[-1].file_id if message.photo else None

    if description == 'Назад':
        await message.answer(
            text='<strong>✅ Вы вернулись в главное меню.</strong>',
            reply_markup=await user_keyboards.main_menu(),
            parse_mode='HTML'
        )
        await state.clear()
        return
    
    if not description and not file_id:
        await message.answer(
            text='❌ <strong>Пожалуйста, опиши свою заявку</strong>',
            parse_mode='HTML'
        )
        return

    description = 'Нет описания' if description == 'Пропустить' else description
    await state.update_data(description=description, file_id=file_id)

    user_choices[message.from_user.id] = {tech: False for tech in TECHS}
    await message.answer(
        text='<strong>Хорошо! Теперь выбери технологии, которые ты хочешь использовать в своём проекте. 🌐</strong>',
        reply_markup=await user_keyboards.build_tech_keyboard(message.from_user.id, user_choices),
        parse_mode='HTML'
    )
    await state.set_state(UserApplications.technologies)


@router.callback_query(UserApplications.technologies, F.data.startswith("toggle:"))
async def toggle_technology(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    tech = callback.data.split(":")[1]
    user_choices[user_id][tech] = not user_choices[user_id][tech]

    await callback.message.edit_reply_markup(
        reply_markup=await user_keyboards.build_tech_keyboard(user_id, user_choices)
    )
    await callback.answer()


@router.callback_query(UserApplications.technologies, F.data == "confirm")
async def confirm_technologies(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    chosen = [tech for tech, selected in user_choices[user_id].items() if selected]

    if not chosen:
        await callback.answer("⚠️ Нужно выбрать хотя бы один вариант", show_alert=True)
        return

    await state.update_data(technologies=chosen)
    await callback.message.delete()
    await callback.message.answer(
        text='<strong>Отлично! Теперь выберите срок выполнения заявки. 📅</strong>',
        reply_markup=await user_keyboards.chose_deadline(),
        parse_mode='HTML'
    )
    await state.set_state(UserApplications.deadline)
    
    
@router.message(UserApplications.deadline)
async def get_deadline(message: Message, state: FSMContext):
    deadline = message.text.strip()
    
    if deadline == 'Назад':
        await message.answer(
            text='<strong>✅ Вы вернулись в главное меню.</strong>',
            reply_markup=await user_keyboards.main_menu(),
            parse_mode='HTML'
        )
        await state.clear()
        return
    
    if deadline not in ['До 1 недели', '1-2 недели', 'Более месяца']:
        await message.answer(
            text='❌ <strong>Пожалуйста, выбери сроки из предложенных вариантов</strong>',
            parse_mode='HTML'
        )
        return

    await state.update_data(deadline=deadline)

    data = await state.get_data()
    service = data.get('service')
    description = data.get('description')
    technologies = data.get('technologies')
    file_id = data.get('file_id')

    if file_id:
        await message.answer_photo(
            photo=file_id,
            caption=f'<strong>Услуга:</strong> {service}\n'
             f'<strong>Описание:</strong> {description}\n'
             f'<strong>Технологии:</strong> {", ".join(technologies)}\n'
             f'<strong>Срок выполнения:</strong> {deadline}',
            reply_markup=await user_keyboards.confirmation(),
            parse_mode='HTML'
        )
    else:
        await message.answer(
            text=f'<strong>Услуга:</strong> {service}\n'
             f'<strong>Описание:</strong> {description}\n'
             f'<strong>Технологии:</strong> {", ".join(technologies)}\n'
             f'<strong>Срок выполнения:</strong> {deadline}',
            reply_markup=await user_keyboards.confirmation(),
            parse_mode='HTML'
        )

    await state.set_state(None)
    
    
@router.callback_query(F.data == "confirm_application")
async def confirm_application(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    
    data = await state.get_data()
    service = data.get('service')
    description = data.get('description')
    technologies = data.get('technologies')
    deadline = data.get('deadline')
    file_id = data.get('file_id')
    user_id = callback.from_user.id

    await add_application(
        user_id=user_id,
        service=service,
        description=description,
        technologies=technologies,
        deadline=deadline,
        screenshot=file_id
    )
    
    application = await get_last_application_by_user(user_id)
    user = await get_user(user_id)
    
    text = f"📌 Новая заявка №{application.get('id')}\n👤 Клиент: {user.get('full_name')}\n📞 Телефон: {user.get('number')}\n🛠 Услуга: {application.get('service')}\n💻 Технологии: {application.get('technologies')}\n📅 Срок выполнения: {application.get('deadline')}\n📝 Описание: {application.get('description')}"
    
    if file_id:
        await callback.bot.send_photo(
            chat_id=int(os.getenv("CHAT_ID")),
            photo=file_id,
            caption=text,
            reply_markup=await user_keyboards.link(user.get('username')),
            parse_mode='HTML'
        )
    else:
        await callback.bot.send_message(
            chat_id=int(os.getenv("CHAT_ID")),
            text=text,
            reply_markup=await user_keyboards.link(user.get('username')),
            parse_mode='HTML'
        )

    await callback.message.answer(
        text='✅ <strong>Ваша заявка успешно отправлена!</strong>\n'
             'Мы свяжемся с вами в ближайшее время.',
        reply_markup=await user_keyboards.main_menu(),
        parse_mode='HTML'
    )
    
    await state.clear()
    
    
@router.callback_query(F.data == "cancel_application")
async def cancel_application(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await callback.message.answer(
        text='❌ <strong>Вы отменили заявку.</strong>',
        reply_markup=await user_keyboards.main_menu(),
        parse_mode='HTML'
    )
    
    await state.clear()