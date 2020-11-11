from server_framework.answer_codes import HTTP_OK
from server_framework.parser import Response, Request
from server_framework.router import Router
from server_framework.server import MainServer


async def test_handler(req: Request) -> Response:
    return Response(status=HTTP_OK, data="""{"kek":2}""")


if __name__ == '__main__':
    router = Router()
    router.add_route("/path", test_handler, methods=["GET"])
    s = MainServer(host="0.0.0.0", port=8081, router=router)
    s.run()
