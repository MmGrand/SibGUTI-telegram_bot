from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: Message):
    await message.answer(f"Привет абитуриент, {message.from_user.full_name}!"
                         f"\nНапишите /menu, чтобы начать.")
