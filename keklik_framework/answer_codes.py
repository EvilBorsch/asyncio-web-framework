class HttpCode:
    def __init__(self, code: int, status: str):
        self.code = code
        self.status = status


HTTP_OK = HttpCode(200, "OK")
HTTP_FORBIDDEN = HttpCode(403, "Forbidden")
HTTP_NOT_FOUND = HttpCode(404, "Not Found")
HTTP_NOT_ALLOWED = HttpCode(405, "Method Not Allowed")
HTTP_INTERNAL_SERVER_ERROR = HttpCode(500, "Internal Server Error")
HTTP_BAD_REQUEST = HttpCode(400, "Bad request")
