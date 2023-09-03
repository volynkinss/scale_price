import asyncio
from for_bot import api_redoubt
from swap_transactions import GraphqlQuery


async def start():
    worker = GraphqlQuery(api_key=api_redoubt)
    await worker.start_swap_checker()
    await worker.start_jetton_transfer_checker()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
