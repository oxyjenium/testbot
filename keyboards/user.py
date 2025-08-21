from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder


async def share_contact():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📱 Отправить контакт", request_contact=True)  
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    

async def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📝 Оставить заявку"),
                KeyboardButton(text="📞 Контакты")
            ],
            [
                KeyboardButton(text="ℹ️ Информация о компании")
            ]
        ],
        resize_keyboard=True
    )
    

async def contact_info():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💬 Написать в поддержку", url="https://t.me/oxyjenium")
            ],
            [
                InlineKeyboardButton(text="🌐 Перейти на сайт", url="https://example.com")
            ]
        ]
    )


async def application_services():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Разработка сайта"),
                KeyboardButton(text="Мобильное приложение")
            ],
            [
                KeyboardButton(text="Техническая поддержка"),
                KeyboardButton(text="Консультация")
            ],
            [
                KeyboardButton(text="Назад")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    

async def miss():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Пропустить"),
                KeyboardButton(text="Назад")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    

  
TECHS = ["Python", "JavaScript", "UI/UX дизайн", "1С интеграция"]

async def build_tech_keyboard(user_id: int, user_choices: dict):
    builder = InlineKeyboardBuilder()
    choices = user_choices.get(user_id, {tech: False for tech in TECHS})

    for tech, selected in choices.items():
        emoji = "✅" if selected else "❌"
        builder.button(
            text=f"{emoji} {tech}",
            callback_data=f"toggle:{tech}"
        )

    builder.button(
        text="✔️ Подтвердить",
        callback_data="confirm"
    )
    
    builder.adjust(1)
    return builder.as_markup()


async def chose_deadline():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="До 1 недели"),
                KeyboardButton(text="1-2 недели")
            ],
            [
                KeyboardButton(text="Более месяца")
            ],
            [
                KeyboardButton(text="Назад")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    

async def confirmation():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Подтвердить",
                    callback_data="confirm_application"
                ),
                InlineKeyboardButton(
                    text="❌ Отменить",
                    callback_data="cancel_application"
                )
            ]
        ]
    )
    
    
async def link(username: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💬 Написать в Telegram",
                    url=f"https://t.me/{username}"
                )
            ]
        ]
    )
