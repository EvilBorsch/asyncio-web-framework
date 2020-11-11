import asyncio

import asyncio_redis

from server_framework.router import Router
from server_framework.server import HTTPServer
from src.converter.delivery.delivery import Converter_handler
from src.converter.repository.repository import Converter_repository
from src.converter.usecase.usecase import Converter_usecase


async def connect_to_redis():
    connection = await asyncio_redis.Connection.create(host='localhost', port=6379)
    return connection



if __name__ == '__main__':
    res=asyncio.get_event_loop().run_until_complete(connect_to_redis())
    print(res)
    router = Router()
    rep = Converter_repository(res)
    ucase = Converter_usecase(rep)
    handler = Converter_handler(router, ucase)
    handler.add_handlers()

    s = HTTPServer(host="0.0.0.0", port=8081, router=router)
    s.run()
