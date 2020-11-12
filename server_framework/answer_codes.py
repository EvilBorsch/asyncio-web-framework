class Http_code:
    def __init__(self, code: int, status: str):
        self.code = code
        self.status = status


HTTP_OK = Http_code(200, "OK")
HTTP_FORBIDDEN = Http_code(403, "Forbidden")
HTTP_NOT_FOUND = Http_code(404, "Not Found")
HTTP_NOT_ALLOWED = Http_code(405, "Method Not Allowed")
HTTP_INTERNAL_SERVER_ERROR = Http_code(500, "Internal Server Error")
HTTP_BAD_REQUEST = Http_code(400, "Bad request")
