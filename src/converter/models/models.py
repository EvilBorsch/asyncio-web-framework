from schematics import Model
from schematics.types import StringType, IntType


class Convert_model(Model):
    currency_from = StringType(required=True)
    currency_to = StringType(required=True, default="USD")
    amount = IntType(required=True)
