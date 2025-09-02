import asyncio
import logging

from aiogram import Bot, Dispatcher

import config as cfg

from handlers import routers
from middleware import DatabaseMiddleware
from db.db import init_db, get_pool, close_pool


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


async def startup():
    logger.info("Бот запускается")


async def shutdown():
    logger.info("Бот отключается")
    

async def main():
    await init_db()
    pool = get_pool()
    db_middleware = DatabaseMiddleware(pool)
    
    dp = Dispatcher()
    bot = Bot(token=cfg.BOT_TOKEN)
    
    dp.include_routers(*routers)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    dp.message.middleware.register(db_middleware)
    dp.callback_query.middleware.register(db_middleware)
    
    try:
        await dp.start_polling(bot)
    finally:
        await pool.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
