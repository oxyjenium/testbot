import keyboards.user as user_keyboards

from aiogram import Router, F
from aiogram.types import Message


router = Router()


@router.message(F.text == 'ℹ️ Информация о компании')
async def company_info(message: Message):
    await message.answer_photo(
        photo='https://i.pinimg.com/736x/08/48/58/084858e17760cdcf8eccb77c6554f978.jpg',
        caption='💻 <strong>Мы – компания, создающая программное обеспечение вашей мечты!</strong>\nНаша команда состоит из <strong>опытных специалистов</strong>, готовых воплотить ваши идеи 💡 и помочь достичь <strong>бизнес-целей</strong> 🚀.',
        parse_mode='HTML'
    )
    

@router.message(F.text == '📞 Контакты')
async def contacts(message: Message):
    await message.answer(
        text='💬 <strong>Если у вас есть вопросы или предложения, не стесняйтесь обращаться к нам!</strong>',
        reply_markup=await user_keyboards.contact_info(),
        parse_mode='HTML'
    )