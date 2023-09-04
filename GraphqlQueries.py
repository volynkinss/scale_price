# 1. console output of dex_swaps result by graphql query - done
# 2. try to get all swaps by last minute - impossible
# 3. output to console average value of every token by src/dst - done

from loguru import logger
from redoubt_agent import RedoubtEventsStream
from resourses.queries import queries
from resourses.swap_operation import OperationDetails
from resourses.Localization import Localization
from decimal import Decimal


class GraphqlQuery:
    def __init__(self, api_key=None):
        self.stream = RedoubtEventsStream(api_key)

    async def get_jetton_transfers(self, obj):
        res = await self.stream.execute(
            queries.JETTON_MASTER_QUERY % obj["data"]["master"]
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
            swap_transaction = Localization.swap_info_msg.format(
                swap_operation.msg_id,
                swap_operation.time,
                swap_operation.platform,
                swap_operation.user,
                src_token_name,
                dst_token_name,
                total_rate,
            )
            logger.info(swap_transaction)

    async def start_jetton_transfer_checker(self):
        logger.info("Running jetton transfer checker")
        await self.stream.subscribe(
            self.get_jetton_transfers, scope="Jetton", event_type="Transfer"
        )

    async def start_swap_checker(self):
        logger.info("Running dex swaps checker")
        await self.get_swap_transactions()
