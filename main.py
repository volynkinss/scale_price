from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from redoubt_agent import RedoubtEventsStream
from for_bot import bot_token, api_redebout
from loguru import logger


bot = Bot(token=bot_token)
dp = Dispatcher(bot)


class JettonTransfersBot:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.stream = RedoubtEventsStream(api_key)

    async def handler(self, obj):
        res = await self.stream.execute(
            """
            query jetton {
                redoubt_jetton_master(where: {address: {_eq:"%s"}}) {
                    address
                    symbol
                    decimals
                    admin_address
                }
            }
        """
            % obj["data"]["master"]
        )
        print(obj)
        print(res)
        if len(res["redoubt_jetton_master"]) == 0:
            logger.info("Jetton master info not found")
        jetton = res["redoubt_jetton_master"][0]
        decimals = jetton.get("decimals", 9)
        if not decimals:
            decimals = 9
        logger.info(
            f"{obj['data']['source_owner']} => {obj['data']['destination_owner']} {int(obj['data']['amount']) / pow(10, decimals)} {jetton['symbol']}"
        )

    async def start_check(self):
        logger.info("Running jetton transfer bot")
        await self.stream.subscribe(self.handler, scope="Jetton", event_type="Transfer")


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Hello everybody")
    worker = JettonTransfersBot(api_key=api_redebout)
    await worker.start_check()


if __name__ == "__main__":
    executor.start_polling(dp)
