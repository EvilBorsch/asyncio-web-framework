import aioredis

from src.converter.exceptions import CurrencyIsNotAdded


class ConverterRepository:
    def __init__(self, connection: aioredis.connection):
        self.connection = connection

    async def get_currency_rate(self, currency_name: str) -> float:
        cur = await self.connection.lindex(currency_name, -1, encoding='utf-8')
        if cur is None:
            raise CurrencyIsNotAdded(currency_name)
        return float(cur)

    async def set_currency_rate(self, currency_name: str, currency_rate: float, merge: bool):
        if merge == 1:
            await self.connection.rpush(currency_name, currency_rate)
        else:
            await self.connection.ltrim(currency_name, -1, -1)
