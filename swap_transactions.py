# 1. console output of dex_swaps result by graphql query
# 2. try to get all swaps by last minute
# 3. output to console average value of every token by src/dst

import asyncio
from for_bot import api_redebout
from loguru import logger
from redoubt_agent import RedoubtEventsStream


class GraphqlQuery:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.stream = RedoubtEventsStream(api_key)

    async def handler(self):
        swaps_info = await self.stream.execute(
            """
            query GetDexSwaps {
                    redoubt_dex_swaps {
                        msg_id
                        platform
                        swap_dst_token
                        swap_src_token
                        swap_dst_amount
                        swap_src_amount
                        swap_time
                        swap_user
                    }
                }
            """
        )
        swaps_info = swaps_info["redoubt_dex_swaps"]
        if len(swaps_info) == 0:
            logger.info("dex swaps not found")
        for index in range(len(swaps_info)):
            swap_info_msg = f"\nSwap id № {swaps_info[index]['msg_id']} at {swaps_info[index]['swap_time']} on {swaps_info[index]['platform']} platform\nby user {swaps_info[index]['swap_user']}:\n{swaps_info[index]['swap_src_amount']} {swaps_info[index]['swap_src_token']} => {swaps_info[index]['swap_dst_amount']} {swaps_info[index]['swap_dst_token']}"
            logger.info(swap_info_msg)

    async def start_check(self):
        logger.info("Running dex swaps checker")
        await self.handler()


async def start():
    worker = GraphqlQuery(api_key=api_redebout)
    await worker.start_check()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
