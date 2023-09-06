from aiogram import types
from aiogram.dispatcher.filters import Command
from bot_setup import bot
from GraphqlQueries import GraphqlQuery
from for_bot import api_redoubt


def setup_handler(dp):
    dp.message_handler(Command("start"))(cmd_start)

async def cmd_start(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text="Let's start monitoring swaps 🙋‍♂️🚀")
    swaps = GraphqlQuery(api_key=api_redoubt, chat_id=chat_id)
    await swaps.start_swap_monitoring()

