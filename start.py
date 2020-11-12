import asyncio

import aioredis

from server_framework.router import Router
from server_framework.server import HTTPServer
from src.converter.delivery.delivery import ConverterHandler
from src.converter.repository.repository import ConverterRepository
from src.converter.usecase.usecase import ConverterUsecase


async def connect_to_redis(url: str = ""):
    redis = await aioredis.create_redis_pool(url)
    return redis


if __name__ == '__main__':
    connection = asyncio.run(connect_to_redis('redis://localhost'))
    router = Router()

    rep = ConverterRepository(connection)
    ucase = ConverterUsecase(rep)
    handler = ConverterHandler(router, ucase)
    handler.add_handlers()

    s = HTTPServer(host="0.0.0.0", port=8081, router=router)
    s.run()
