import asyncio
from for_bot import api_redoubt
from GraphqlQueries import GraphqlQuery
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot_setup import bot
from aiogram.utils import executor
from actions_for_bor import setup_handler

storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

setup_handler(dp)


async def start():
    worker = GraphqlQuery(api_key=api_redoubt)
    await worker.start_swap_monitoring()


if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(start())
    executor.start_polling(dp)
