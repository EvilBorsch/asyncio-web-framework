from keklik_framework.exceptions import RouteIsNotExist, MethodNotAllowedException
from keklik_framework.parser import Request


class HandlerMethodInfo:
    def __init__(self, handler, methods: list):
        self.handler = handler
        self.methods = methods


class Router:
    # TODO TypedDict
    routes = dict()

    def __init__(self, base_route: str = "/api"):
        self.base_route = base_route

    def add_route(self, route: str, handler, methods: list):
        """
        Добавление нового роута
        :param route: Путь по которому будет доступен handler
        :param handler: Сам handler(Функция принимающая Request и возвразающая Response
        :return:
        """
        route = self.base_route + route
        self.routes[route] = HandlerMethodInfo(handler=handler, methods=methods)

    async def navigate(self, request: Request):
        """
        Вызов по заданному пути handlerа
        :param path:
        :param request:
        :return:
        """
        route = self.base_route + request.path
        try:
            handler_methods_info = self.routes[route]
        except KeyError:
            raise RouteIsNotExist(route)
        if request.method not in handler_methods_info.methods:
            raise MethodNotAllowedException(request.method)
        return await handler_methods_info.handler(request)
