from server_framework.answer_codes import HTTP_OK
from server_framework.parser import Response


def get_ok_response(data: str):
    res = "{" + data + "}"
    return Response(status=HTTP_OK, data=res)
