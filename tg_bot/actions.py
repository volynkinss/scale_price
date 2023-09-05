from aiogram import types
from aiogram.dispatcher.filters import Command
from bot_setup import bot


async def show_swap_monitoring(chat_id: int):
    await bot.send_message(chat_id=chat_id, text="hello")


async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    show_swap_monitoring(user_id)
