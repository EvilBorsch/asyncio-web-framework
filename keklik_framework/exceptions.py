class MethodNotAllowedException(Exception):
    def __init__(self, method):
        self.method = method

    def __str__(self):
        return f"Method {self.method} is not allowed"


class RouteIsNotExist(Exception):
    def __init__(self, route):
        self.route = route

    def __str__(self):
        return f"Route {self.route} is not exist"


class IncorrectJsonError(Exception):
    def __init__(self, json):
        self.json = json

    def __str__(self):
        return f"Json {self.json} is incorrect"
