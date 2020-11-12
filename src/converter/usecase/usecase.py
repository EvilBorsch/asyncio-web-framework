from src.converter.repository.repository import ConverterRepository


class ConverterUsecase:
    def __init__(self, repository: ConverterRepository):
        self.repository = repository

    async def convert_currencys(self, currency_from: str, currency_to: str, amount: float) -> float:
        if currency_from != currency_to:
            cur_from = await self.repository.get_currency_rate(currency_from)
            cur_to = await self.repository.get_currency_rate(currency_to)
            converted_value = amount * (cur_from / cur_to)
        else:
            converted_value = amount
        return converted_value

    async def add_currencys(self, currency_name: str, currency_rate: float, merge: bool) -> str:
        await self.repository.set_currency_rate(currency_name, currency_rate, merge)
        if merge:
            return f"Add new value of {currency_name} -> {currency_rate}"
        else:
            return f"Old values is deleted"
