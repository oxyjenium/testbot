from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def make_user_keyboard(page: int, users, total_pages: int):
    keyboard = []
    for user in users:
        keyboard.append([InlineKeyboardButton(
            text=user["username"],
            callback_data=f"user:{user['tg_id']}"
        )])

    nav_buttons = []

    prev_page = page - 1 if page > 1 else total_pages
    nav_buttons.append(
        InlineKeyboardButton(text="⬅ Назад", callback_data=f"page:{prev_page}")
    )

    nav_buttons.append(
        InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="none")
    )

    next_page = page + 1 if page < total_pages else 1
    nav_buttons.append(
        InlineKeyboardButton(text="Вперед ➡", callback_data=f"page:{next_page}")
    )

    keyboard.append(nav_buttons)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def make_application_keyboard(page: int, applications, total_pages: int):
    keyboard = []
    for app in applications:
        keyboard.append([InlineKeyboardButton(
            text=str(app["id"]),
            callback_data=f"application:{app['id']}"
        )])

    nav_buttons = []

    prev_page = page - 1 if page > 1 else total_pages
    nav_buttons.append(
        InlineKeyboardButton(text="⬅ Назад", callback_data=f"aplication_page:{prev_page}")
    )

    nav_buttons.append(
        InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="none")
    )

    next_page = page + 1 if page < total_pages else 1
    nav_buttons.append(
        InlineKeyboardButton(text="Вперед ➡", callback_data=f"aplication_page:{next_page}")
    )

    keyboard.append(nav_buttons)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
