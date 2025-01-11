import asyncio
import logging
import time
from typing import Type

import aiohttp

from logger_config import setup_logger
from settings import Settings


logger = setup_logger(__name__, "request.log", level=logging.INFO)

def get_user_input(prompt: str, default_value: str, value_type: Type) -> Type:
    while True:
        user_input = input(f"{prompt} (по умолчанию: {default_value}): ").strip()
        if not user_input:
            return value_type(default_value)
        try:
            return value_type(user_input)
        except ValueError:
            print(f"Ошибка: ожидалось значение типа {value_type.__name__}. Попробуйте ещё раз.")

def load_settings() -> Settings:
    settings = Settings()

    number_of_requests = get_user_input(
        "Введите количество запросов", settings.number_of_requests, int
    )
    total_time = get_user_input(
        "Введите время выполнения (в секундах)", settings.total_time, int
    )
    ip_address = get_user_input(
        "Введите IP-адрес", settings.ip_address, str
    )
    port = get_user_input(
        "Введите порт", settings.port, int
    )

    return Settings(
        number_of_requests=number_of_requests,
        total_time=total_time,
        ip_address=ip_address,
        port=port,
        endpoint=settings.endpoint,
    )


settings = load_settings()

url = f"http://{settings.ip_address}:{settings.port}/{settings.endpoint}"
interval = settings.total_time / settings.number_of_requests

async def send_request(session: aiohttp.ClientSession) -> None:
    try:
        async with session.get(url) as response:
            logger.info(f"Статус ответа: {response.status}, Ответ: {await response.text()}")
    except aiohttp.ClientError as e:
        logger.error(f"Ошибка клиента: {e}")
    except asyncio.TimeoutError:
        logger.error("Время ожидания запроса истекло")
    except Exception as e:
        logger.error(f"Непредвиденная ошибка: {e}")

async def main() -> None:
    async with aiohttp.ClientSession() as session:
        for _ in range(settings.number_of_requests):
            start_time = time.monotonic()
            await send_request(session)
            elapsed_time = time.monotonic() - start_time
            sleep_time = interval - elapsed_time
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)


if __name__ == "__main__":
    asyncio.run(main())
