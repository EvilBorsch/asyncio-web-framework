from schematics import Model
from schematics.types import StringType, IntType, FloatType


class ConvertModel(Model):
    currency_from = StringType(required=True)
    currency_to = StringType(required=True, default="USD")
    amount = IntType(required=True)


class SetCurrencyModel(Model):
    currency_name = StringType(required=True)
    currency_rate = FloatType(required=True)
