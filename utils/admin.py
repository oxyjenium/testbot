import asyncio

from aiogram.types import Message


async def delete_message_with_timeout(timeout: int, message: Message):
    await asyncio.sleep(timeout)
    await message.delete()