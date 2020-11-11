from server_framework.parser import Request, Response
from server_framework.router import Router
from src.converter.usecase.usecase import Converter_usecase
from src.utills import get_ok_response


class Converter_handler:
    def __init__(self, router: Router, usecase: Converter_usecase):
        self.router = router
        self.usecase = usecase

    async def get_currency_handler(self, req: Request) -> Response:
        currency_from = req.params.get("from")
        currency_to = req.params.get("to")
        amount = float(req.params.get("amount"))
        res = await self.usecase.convert_currencys(currency_from, currency_to, amount)
        return get_ok_response(str(res))

    def add_handlers(self):
        self.router.add_route("/convert", self.get_currency_handler, methods=["GET"])
