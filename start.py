import os

import aioredis
import asyncio

from keklik_framework.router import Router
from keklik_framework.server import HTTPServer
from src.converter.delivery.delivery import ConverterHandler
from src.converter.repository.repository import ConverterRepository
from src.converter.usecase.usecase import ConverterUsecase


async def connect_to_redis(url: str):
    redis = await aioredis.create_redis_pool(url)
    return redis


if __name__ == '__main__':
    redis_url = os.environ.get("REDIS_URL", "redis://localhost")
    connection = asyncio.run(connect_to_redis(redis_url))
    router = Router()

    rep = ConverterRepository(connection)
    ucase = ConverterUsecase(rep)
    handler = ConverterHandler(router, ucase)
    handler.add_handlers()

    s = HTTPServer(host="0.0.0.0", port=8081, router=router)
    s.run()
