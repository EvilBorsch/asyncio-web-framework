from src.converter.repository.repository import Converter_repository


class Converter_usecase:
    def __init__(self, repository: Converter_repository):
        self.repository = repository

    async def convert_currencys(self, currency_from: str, currency_to: str, amount: float) ->float:
        cur_from = await self.repository.get_currency_rate(currency_from)
        cur_to = await self.repository.get_currency_rate(currency_to)
        converted_value = amount * (cur_from / cur_to)
        return converted_value
