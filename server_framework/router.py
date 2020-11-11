from server_framework.parser import Request


class Router:
    # TODO TypedDict
    routes = dict()

    def add_route(self, route: str, handler):
        """
        Добавление нового роута
        :param route: Путь по которому будет доступен handler
        :param handler: Сам handler(Функция принимающая Request и возвразающая Response
        :return:
        """
        self.routes[route] = handler

    async def navigate(self, path: str, request: Request):
        """
        Вызов по заданному пути handlerа
        :param path:
        :param request:
        :return:
        """
        handler = self.routes[path]
        return await handler(request)
