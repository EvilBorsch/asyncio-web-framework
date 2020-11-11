import aioredis


class Converter_repository:
    def __init__(self, connection: aioredis.connection):
        self.connection = connection

    async def get_currency_rate(self, currency_name: str) -> float:
        cur=await self.connection.get(currency_name)
        return cur
