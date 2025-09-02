from aiogram.filters import BaseFilter
from aiogram.types import Message

import config as cfg


class IsAdmin(BaseFilter):
    async def __call__(self, msg: Message) -> bool:
        return msg.from_user.id in cfg.ADMIN_LIST
