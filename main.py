import asyncio
from for_bot import api_redoubt
from GraphqlQueries import GraphqlQuery


async def start():
    worker = GraphqlQuery(api_key=api_redoubt)
    await worker.start_swap_monitoring()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
