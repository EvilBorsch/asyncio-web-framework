from server_framework.answer_codes import HTTP_OK, Http_code
from server_framework.parser import Response


def get_ok_response(data: str):
    res = {"Data": data, "Error": "NULL"}
    return Response(status=HTTP_OK, data=res)


def get_error_response(status: Http_code, message: str):
    data = {"Data": "NULL", "Error": message}
    return Response(status=status, data=data)
