import re
import asyncpg

from datetime import datetime

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import keyboards.user as user_keyboards

from db.crud import create_user, update_user_details, check_user_fields
from states import UserRegistration


router = Router()


DATE_PATTERN = re.compile(r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19|20)\d\d$")


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    try:
        await create_user(
            tg_id=message.from_user.id,
            username=message.from_user.username
        )
    except asyncpg.exceptions.UniqueViolationError:
        if await check_user_fields(tg_id=message.from_user.id):
            await message.answer(
                text='👋 Привет! Ты уже зарегистрирован в нашем боте.',
                reply_markup=user_keyboards.main_menu(),
                parse_mode='HTML'
            )
            return
        else:
            pass
        
        
    await message.answer(
        text='Привет! 👋 Это <strong>тестовый бот</strong>, в котором тебе нужно пройти регистрацию.\nДля начала введи своё <strong>ФИО</strong> 📝',
        parse_mode='HTML'
    )
    await state.set_state(UserRegistration.full_name)
    

@router.message(UserRegistration.full_name)
async def get_full_name(message: Message, state: FSMContext):
    full_name = message.text.strip()
    
    if len(full_name.split()) != 3:
        await message.answer(
            text='✍️ <strong>Пожалуйста, введи своё полное имя</strong>\n(Фамилия, Имя и Отчество) 📝',
            parse_mode='HTML'
        )
        return

    await state.update_data(full_name=full_name)
    await message.answer(
        text='🎂 <strong>Отлично!</strong>\nТеперь введи <strong>свою дату рождения</strong> в формате <strong>ДД.ММ.ГГГГ</strong> 📅',
        parse_mode='HTML'
    )
    await state.set_state(UserRegistration.date_birth)
    

@router.message(UserRegistration.date_birth)
async def get_date_birth(message: Message, state: FSMContext):
    date_birth = message.text.strip()

    if not DATE_PATTERN.match(date_birth):
        await message.answer(
            text='❌ <strong>Неверный формат даты!</strong>\nПожалуйста, введи дату в формате <strong>ДД.ММ.ГГГГ</strong> 📅\nПример: <strong>03.10.2000</strong> ✅',
            parse_mode='HTML'
        )
        return
    
    user_date = datetime.strptime(date_birth, "%d.%m.%Y")
    now_date = datetime.now()

    if user_date > now_date:
        await message.answer(
            text='❌ <strong>Дата рождения не может быть в будущем!</strong>\nПожалуйста, введи корректную дату в формате <strong>ДД.ММ.ГГГГ</strong> 📅',
            parse_mode='HTML'
        )
        return

    await state.update_data(date_birth=date_birth)
    
    await message.answer(
        text='📲 <strong>Отлично!</strong>\nТеперь, пожалуйста, <strong>поделись своим контактом</strong>, чтобы мы могли с тобой связаться.',
        reply_markup=user_keyboards.share_contact(),
        parse_mode='HTML'
    )
    await state.set_state(UserRegistration.number)
    

@router.message(UserRegistration.number, F.contact)
async def get_contact(message: Message, state: FSMContext):
    contact = message.contact

    if not contact or not contact.phone_number:
        await message.answer("Пожалуйста, поделись своим контактом")
        return

    data = await state.get_data()
    full_name = data.get('full_name')
    date_birth = data.get('date_birth')

    await update_user_details(
        tg_id=message.from_user.id,
        full_name=full_name,
        date_birth=datetime.strptime(date_birth, "%d.%m.%Y").date(),
        number=contact.phone_number
    )

    await message.answer(
        text=f'✅ <strong>Регистрация завершена!</strong>\n👤 <strong>ФИО:</strong> {full_name}\n🎂 <strong>Дата рождения:</strong> {date_birth}\n📞 <strong>Номер телефона:</strong> {contact.phone_number}\n🙏 Спасибо за предоставленную информацию!',
        reply_markup=user_keyboards.main_menu(),
        parse_mode='HTML'
    )
    await state.clear()
 