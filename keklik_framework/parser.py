import json
from datetime import datetime
from email.message import Message
from email.parser import BytesParser
from time import mktime
from typing import Any
from wsgiref.handlers import format_date_time

from keklik_framework.answer_codes import HttpCode
from keklik_framework.exceptions import IncorrectJsonError

ENCODING = "iso-8859-1"


def get_date():
    now = datetime.now()
    stamp = mktime(now.timetuple())
    return format_date_time(stamp)


def get_params(url: str) -> (str, dict):
    """
    Вовзращает часть урал до ? и дикт из гет параметров
    :param url:
    :return:
    """
    ans = dict()
    splited = url.split("?")
    path = splited[0]
    try:
        params = splited[1]
    except IndexError:
        return path, dict()
    params = params.split("&")
    for param in params:
        key, value = param.split("=")
        ans[key] = value
    return path, ans


def parse(raw: bytes):
    try:
        request_line, headers_alone = raw.split(b'\r\n', 1)
    except:
        return None
    headers = BytesParser().parsebytes(headers_alone)
    body = headers.get_payload()
    parsed_body = {}
    if body != "":
        try:
            parsed_body = json.loads(body)
        except Exception as e:
            raise IncorrectJsonError(body)
    method, url, ver = request_line.decode(ENCODING).split()
    path, params = get_params(url)
    return Request(method, path, ver, headers, params, parsed_body)


class Request:
    def __init__(self, method: str, path: str, version: str, headers: Message, params: dict, body: dict):
        self.method = method
        self.path = path
        self.version = version
        self.headers = headers
        self.params = params
        self.body = body

    def __str__(self):
        return f'Method: {self.method} Path: {self.path}\n'


class Response:
    # TODO strings to byte
    def __init__(self, status: HttpCode, data: Any, typ="json"):
        self.status = status
        self.path = None
        self.data = data
        self.type = typ

    def get_answer(self) -> str:
        """
        В дальнейшем функция должна поддерживать и другие типы ответа
        :return: Http answer
        """
        if self.type.lower() == "json":
            return self.get_json_answer()
        return self.get_json_answer()

    def get_json_answer(self) -> str:
        json_data = json.dumps(self.data)
        ans = f"""HTTP/1.1 {self.status.code} {self.status.status}
                Content-Length: {len(json_data) - 1}
                Connection: close
                Content-Type: application/json

{json_data}
"""
        ans += '\r\n'
        return ans


def get_error(status: HttpCode, message: str):
    data = "{\n\"Error\":\"" + message + "\"\n}"
    ans = f"""HTTP/1.1 {status.code} {status.status}
            Content-Length: {len(data) - 1}
            Connection: close
            Content-Type: application/json

{data}
    """
    ans += '\r\n'
    return ans
