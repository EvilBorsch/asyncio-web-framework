from keklik_framework.answer_codes import HTTP_OK, HttpCode
from keklik_framework.parser import Response


def get_ok_response(data: str):
    res = {"Data": data, "Error": "NULL"}
    return Response(status=HTTP_OK, data=res)


def get_error_response(status: HttpCode, message: str):
    data = {"Data": "NULL", "Error": message}
    return Response(status=status, data=data)
