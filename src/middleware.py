from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from asyncpg.pool import Pool


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, db_pool: Pool):
        super().__init__()
        self.db_pool = db_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        data['pool'] = self.db_pool
        return await handler(event, data)