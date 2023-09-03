# 1. console output of dex_swaps result by graphql query - done
# 2. try to get all swaps by last minute - impossible
# 3. output to console average value of every token by src/dst - done

import asyncio
from for_bot import api_redoubt
from loguru import logger
from redoubt_agent import RedoubtEventsStream
from resourses.queries import queries
from resourses.swap_operation import OperationDetails
from resourses.Localization import Localization
from decimal import Decimal


class GraphqlQuery:
    def __init__(self, api_key=None):
        self.stream = RedoubtEventsStream(api_key)

    async def get_jetton_name(self, address):
        jetton_name_query = await self.stream.execute(
            queries.JETTON_NAME_QUERY % address
        )
        jetton_name_query_result = jetton_name_query["redoubt_jetton_master"]
        if jetton_name_query_result == []:
            name = "UNKWN Coin"
        else:
            name = jetton_name_query_result[0]["name"]
        return name

    async def get_swap_transactions(self):
        swaps_info = await self.stream.execute(queries.DEX_SWAPS_QUERY)
        swaps_info = swaps_info["redoubt_dex_swaps"]
        if len(swaps_info) == 0:
            logger.info("dex swaps not found")
            return
        for index in range(len(swaps_info)):
            swap_operation = OperationDetails(swaps_info[index])
            src_token_name = await self.get_jetton_name(swap_operation.src_token)
            dst_token_name = await self.get_jetton_name(swap_operation.dst_token)
            total_rate = Decimal(swap_operation.src_amount) / Decimal(
                swap_operation.dst_amount
            )
            result = Localization.swap_info_msg.format(
                swap_operation.msg_id,
                swap_operation.formatted_time(),
                swap_operation.platform,
                swap_operation.user,
                src_token_name,
                dst_token_name,
                total_rate,
            )
            logger.info(result)

    async def start_check(self):
        logger.info("Running dex swaps checker")
        await self.get_swap_transactions()


async def start():
    worker = GraphqlQuery(api_key=api_redoubt)
    await worker.start_check()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
