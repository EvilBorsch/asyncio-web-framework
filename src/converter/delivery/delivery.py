import schematics
from schematics.exceptions import DataError

from keklik_framework.answer_codes import HTTP_BAD_REQUEST
from keklik_framework.parser import Request, Response
from keklik_framework.router import Router
from src.converter.exceptions import CurrencyIsNotAdded
from src.converter.models.models import SetCurrencyModel, ConvertModel
from src.converter.usecase.usecase import ConverterUsecase
from src.utills import get_ok_response, get_error_response


class ConverterHandler:
    def __init__(self, router: Router, usecase: ConverterUsecase):
        self.router = router
        self.usecase = usecase

    def add_handlers(self):
        self.router.add_route("/convert", self.get_currency_handler, methods=["GET"])
        self.router.add_route("/database", self.set_currency_handler, methods=["POST"])

    async def get_currency_handler(self, req: Request) -> Response:
        curr_model = ConvertModel({"currency_from": req.params.get("from"),
                                   "currency_to": req.params.get("to"),
                                   "amount": req.params.get("amount")})
        try:
            curr_model.validate()
        except schematics.exceptions.BaseError as e:
            return get_error_response(HTTP_BAD_REQUEST, str(e))
        try:
            res = await self.usecase.convert_currencys(curr_model.currency_from, curr_model.currency_to,
                                                       curr_model.amount)
        except CurrencyIsNotAdded as e:
            return get_error_response(HTTP_BAD_REQUEST, str(e))
        return get_ok_response(str(res))

    async def set_currency_handler(self, req: Request) -> Response:
        merge_raw = req.params.get("merge")
        if merge_raw is not None:
            merge = (merge_raw.lower() == "true" or merge_raw == "1")
        else:
            merge = True
        set_model = SetCurrencyModel(req.body)
        try:
            set_model.validate()
        except schematics.exceptions.BaseError as e:
            return get_error_response(status=HTTP_BAD_REQUEST, message="Incorrect json with error:" + str(e))
        res = await self.usecase.add_currencys(currency_name=set_model.currency_name,
                                               currency_rate=set_model.currency_rate, merge=merge)
        return get_ok_response(res)
