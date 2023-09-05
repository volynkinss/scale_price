# 1. console output of dex_swaps result by graphql query - done
# 2. try to get all swaps by last minute - impossible
# 3. output to console average value of every token by src/dst - done

from loguru import logger
from redoubt_agent import RedoubtEventsStream
from resourses.queries import queries, SCOPE, EVENT_TYPE
from resourses.swap_operation import OperationDetails, DexSwapDetails
from resourses.Localization import Localization
from resourses.jetton_transfers import JettonTranfer
from decimal import Decimal
from tg_bot.actions import show_swap_monitoring


class GraphqlQuery:
    def __init__(self, api_key=None):
        self.stream = RedoubtEventsStream(api_key)

    async def get_jetton_transfers(self, transfers_info):
        transfer = JettonTranfer(transfers_info)
        jetton_master_query_result = await self.stream.execute(
            queries.JETTON_MASTER_QUERY % transfer.master
        )
        redoubt_jetton_master = jetton_master_query_result["redoubt_jetton_master"]
        if len(redoubt_jetton_master) == 0:
            logger.info("Jetton master info not found")
        jetton = redoubt_jetton_master[0]
        symbol = jetton["symbol"]
        decimals = jetton.get("decimals", 9)
        if not decimals:
            decimals = 9
        readble_transfer_amount = transfer.amount / pow(10, decimals)
        logger.info(
            Localization.jetton_transfer_msg.format(
                transfer.source_owner,
                transfer.destination_owner,
                readble_transfer_amount,
                symbol,
            )
        )

    async def get_jetton_name(self, address):
        jetton_name_query = await self.stream.execute(
            queries.JETTON_NAME_QUERY % address
        )
        jetton_name_query_result = jetton_name_query["redoubt_jetton_master"]
        name = (
            "UNKWN Coin"
            if jetton_name_query_result == []
            else jetton_name_query_result[0]["name"]
        )
        return name

    async def get_swap_transactions(self):
        dex_swaps_query_result = await self.stream.execute(queries.DEX_SWAPS_QUERY)
        swaps_info = dex_swaps_query_result["redoubt_dex_swaps"]
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

    async def swap_monitoring(self, data):
        swap = DexSwapDetails(data)
        name_token_out = await self.get_jetton_name(swap.token_out)
        name_token_in = await self.get_jetton_name(swap.token_in)
        swap_monitoring = Localization.swap_monitoring_msg.format(
            swap.amount_out, name_token_out, swap.amount_in, name_token_in, swap.user
        )
        logger.info(swap_monitoring)
        await show_swap_monitoring()

    async def start_jetton_transfer_checker(self):
        logger.info("Running jetton transfer checker")
        await self.stream.subscribe(
            self.get_jetton_transfers, scope=SCOPE, event_type=EVENT_TYPE
        )

    async def start_swap_checker(self):
        logger.info("Running dex swaps checker")
        await self.get_swap_transactions()

    async def start_swap_monitoring(self):
        logger.info("Running swap monitoring")
        await self.stream.subscribe(
            self.swap_monitoring, scope="DEX", event_type="Swap"
        )
