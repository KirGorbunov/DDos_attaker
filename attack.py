import asyncio
import logging
import aiohttp
import time
from logger_config import setup_logger

logger = setup_logger(__name__, "request.log", level=logging.INFO)

url = "http://127.0.0.1:8000/DDos_test"

def get_positive_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Ошибка: Введите корректное целое положительное число.")


number_of_requests = get_positive_int("Введите необходимое количество запросов: ")
total_time = get_positive_int("Введите время за которое необходимо отправить запросы (в секундах): ")

interval = total_time / number_of_requests

async def send_request(session: aiohttp.ClientSession) -> None:
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
    async with aiohttp.ClientSession() as session:
        for i in range(number_of_requests):
            print(i)
            start_time = time.monotonic()
            await send_request(session)
            elapsed_time = time.monotonic() - start_time
            sleep_time = interval - elapsed_time
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)

if __name__ == "__main__":
    asyncio.run(main())