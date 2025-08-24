from aiogram.filters import BaseFilter
from aiogram.types import Message

import config as cfg


class IsAdmin(BaseFilter):
    async def __call__(self, msg: Message) -> bool:
        admin_ids = cfg.ADMIN
        admin_list = [int(a.strip()) for a in admin_ids.split(",") if a.strip().isdigit()]
        return msg.from_user.id in admin_list
