from server_framework.parser import Request


class HandlerMethodInfo:
    def __init__(self, handler, methods: list):
        self.handler = handler
        self.methods = methods


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


class Router:
    # TODO TypedDict
    routes = dict()

    def add_route(self, route: str, handler, methods: list):
        """
        Добавление нового роута
        :param route: Путь по которому будет доступен handler
        :param handler: Сам handler(Функция принимающая Request и возвразающая Response
        :return:
        """
        self.routes[route] = HandlerMethodInfo(handler=handler, methods=methods)

    async def navigate(self, request: Request):
        """
        Вызов по заданному пути handlerа
        :param path:
        :param request:
        :return:
        """
        try:
            handler_methods_info = self.routes[request.path]
        except KeyError:
            raise RouteIsNotExist(request.path)
        if request.method not in handler_methods_info.methods:
            raise MethodNotAllowedException(request.method)
        return await handler_methods_info.handler(request)
