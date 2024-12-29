import asyncio
import logging

import aiohttp

from logger_config import setup_logger


logger = setup_logger(__name__, "request.log", level=logging.INFO)

url = "http://127.0.0.1:8000/DDos_test"

rate = 15
interval = 1 / rate

async def send_request(session: aiohttp.ClientSession, queue: asyncio.Queue) -> None:
    while True:
        await queue.get()
        try:
            async with session.get(url) as response:
                logger.info(f"Status Code: {response.status}, Response: {await response.text()}")
        except aiohttp.ClientError as e:
            logger.error(f"Client error: {e}")
        except asyncio.TimeoutError:
            logger.error("Request timed out")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

async def main() -> None:
    queue = asyncio.Queue(maxsize=rate * 2)

    async with aiohttp.ClientSession() as session:
        [asyncio.create_task(send_request(session, queue)) for _ in range(rate)]

        while True:
            await queue.put(1)
            await asyncio.sleep(interval)

if __name__ == "__main__":
    asyncio.run(main())
