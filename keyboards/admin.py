from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


async def main_menu_admin():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Статистика пользователей",
                    callback_data="users_stats"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Статистика заявок",
                    callback_data="applications_stats"
                ),
            ],
             [
                InlineKeyboardButton(
                    text="Общая статистика",
                    callback_data="all_stats"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Рассылка",
                    callback_data="mailing"
                )
            ]
        ]
    )
    

async def back_to_list_users():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data="users_stats"
                ),
            ],
        ]
    )
    
    
async def back_to_list_applications():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data="applications_stats"
                ),
            ],
        ]
    )
    

async def back_to_main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Назад в главное меню",
                    callback_data="main_menu_admin"
                ),
            ],
        ]
    )
    

async def mailing_time():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="1 минута", 
                    callback_data="view_set_timer:60",
                ),
                InlineKeyboardButton(
                    text="5 минут", 
                    callback_data="view_set_timer:300",
                ),
                InlineKeyboardButton(
                    text="10 минут", 
                    callback_data="view_set_timer:600",
                ),
                InlineKeyboardButton(
                    text="15 минут", 
                    callback_data="view_set_timer:900",
                ),
                InlineKeyboardButton(
                    text="1 секунда", 
                    callback_data="view_set_timer:1",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data="main_menu_admin"
                ),
            ]
        ]
    )
    

async def mailing_delete_time():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="1 час", 
                    callback_data="view_set_delete_timer:3600",
                ),
                InlineKeyboardButton(
                    text="3 часа", 
                    callback_data="view_set_delete_timer:10800",
                ),
                InlineKeyboardButton(
                    text="6 часов", 
                    callback_data="view_set_delete_timer:21600",
                ),
                InlineKeyboardButton(
                    text="12 часов", 
                    callback_data="view_set_delete_timer:43200",
                ),
                InlineKeyboardButton(
                    text="10 секунд", 
                    callback_data="view_set_delete_timer:10",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data="main_menu_admin"
                ),
            ]
        ]
    )
    

async def confirm_mailing():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Подтвердить",
                    callback_data="confirm_mailing"
                ),
                InlineKeyboardButton(
                    text="❌ В главное меню",
                    callback_data="main_menu_admin"
                )
            ]
        ]
    )