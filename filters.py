import os

from aiogram.filters import BaseFilter
from aiogram.types import Message



class IsAdmin(BaseFilter):
    async def __call__(self, msg: Message) -> bool:
        admin_ids = os.getenv("ADMIN")
        admin_list = [int(a.strip()) for a in admin_ids.split(",") if a.strip().isdigit()]
        return msg.from_user.id in admin_list
