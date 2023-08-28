# 1. console output of dex_swaps result by graphql query
# 2. try to get all swaps by last minute
# 3. output to console average value of every token by src/dst

import asyncio
from for_bot import api_redebout
from loguru import logger
from redoubt_agent import RedoubtEventsStream
from queries import queries
from decimal import Decimal


class GraphqlQuery:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.stream = RedoubtEventsStream(api_key)

    async def get_jetton_name(self, address):
        query = queries()
        jetton_name_query = await self.stream.execute(query.jetton_name_query(address))
        if jetton_name_query["redoubt_jetton_master"] == []:
            name = "UKWN Coin"
        else:
            name = jetton_name_query["redoubt_jetton_master"][0]["name"]
        return name

    async def get_swap_transactions(self):
        query = queries()
        swaps_info = await self.stream.execute(query.dex_swaps_query())
        swaps_info = swaps_info["redoubt_dex_swaps"]
        if len(swaps_info) == 0:
            logger.info("dex swaps not found")
            return
        for index in range(len(swaps_info)):
            swap_operation = swaps_info[index]
            src_token_name = await self.get_jetton_name(
                swap_operation["swap_src_token"]
            )
            dst_token_name = await self.get_jetton_name(
                swap_operation["swap_dst_token"]
            )
            total_rate = Decimal(swap_operation["swap_src_amount"]) / Decimal(
                swap_operation["swap_dst_amount"]
            )
            swap_info_msg = f"""\nSwap id № {swap_operation['msg_id']} at {swap_operation['swap_time']} on {swap_operation['platform']} platform
by user {swap_operation['swap_user']}:
{src_token_name} => {dst_token_name} at a rate of {total_rate}"""
            logger.info(swap_info_msg)

    async def start_check(self):
        logger.info("Running dex swaps checker")
        await self.get_swap_transactions()


async def start():
    worker = GraphqlQuery(api_key=api_redebout)
    await worker.start_check()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
