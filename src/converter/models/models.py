from schematics import Model
from schematics.types import StringType, FloatType


class ConvertModel(Model):
    currency_from = StringType(required=True)
    currency_to = StringType(required=True, default="USD")
    amount = FloatType(required=True)


class SetCurrencyModel(Model):
    currency_name = StringType(required=True)
    currency_rate = FloatType(required=True)
