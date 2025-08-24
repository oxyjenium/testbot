import asyncio

from aiogram import Bot, Dispatcher

import config as cfg

from handlers import routers
from db.db import init_db


async def startup():
    print("Бот запускается")


async def shutdown():
    print("Бот отключается")
    

async def main():
    await init_db()
    dp = Dispatcher()
    bot = Bot(token=cfg.BOT_TOKEN)
    dp.include_routers(*routers)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())
