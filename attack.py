import asyncio
from asyncio import Queue

import aiohttp
from aiohttp import ClientSession


url = "http://127.0.0.1:8000/DDos_test"

rate = 15
interval = 1 / rate

async def send_request(session: ClientSession, queue: Queue) -> None:
    while True:
        await queue.get()
        async with session.get(url) as response:
            print(f"Status Code: {response.status}, Response: {await response.text()}")

async def main() -> None:
    queue = asyncio.Queue(maxsize=rate * 2)

    async with aiohttp.ClientSession() as session:
        [asyncio.create_task(send_request(session, queue)) for _ in range(rate)]

        while True:
            await queue.put(1)
            await asyncio.sleep(interval)

if __name__ == "__main__":
    asyncio.run(main())
