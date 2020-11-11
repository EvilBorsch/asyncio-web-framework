from datetime import datetime
from email.message import Message
from email.parser import BytesParser
from time import mktime
from wsgiref.handlers import format_date_time

from server_framework.answer_codes import Http_code

ENCODING = 'iso-8859-1'


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
    path, params = url.split("?")
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

    method, url, ver = request_line.decode(ENCODING).split()
    path, params = get_params(url)

    return Request(method, path, ver, headers, params)


class Request:
    def __init__(self, method: str, path: str, version: str, headers: Message, params: dict):
        self.method = method
        self.path = path
        self.version = version
        self.headers = headers
        self.params = params
        print(self.params)

    def __str__(self):
        return f'Method: {self.method}\nPath: {self.path}\nVer: {self.version}\n\n'


class Response:
    # TODO strings to byte
    def __init__(self, status: Http_code, data: str, typ="json"):
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
        ans = f"""HTTP/1.1 {self.status.code} {self.status.status}
                Content-Length: {len(self.data) - 1}
                Connection: close
                Content-Type: application/json

                {self.data}
                """
        ans += '\r\n'
        return ans


def get_error(status_code: Http_code, message: str):
    data = "{\nError: " + message + "\n}"
    ans = f"""HTTP/1.1 {status_code.code} {status_code.status}
            Content-Length: {len(data) - 1}
            Connection: close
            Content-Type: application/json

            {data}
            """
    ans += '\r\n'
    return ans
