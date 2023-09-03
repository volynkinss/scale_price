import asyncio
from redoubt_agent import RedoubtEventsStream
from for_bot import api_redoubt
from loguru import logger


class JettonTransfersBot:
    def __init__(self, api_key=None):
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


async def start():
    worker = JettonTransfersBot(api_key=api_redoubt)
    await worker.start_check()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
