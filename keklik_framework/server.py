import os
import socket

import asyncio
import uvloop

from keklik_framework.answer_codes import HTTP_INTERNAL_SERVER_ERROR
from keklik_framework.logger import log
from keklik_framework.parser import parse, ENCODING, get_error
from keklik_framework.router import Router


class HTTPServer:
    def __init__(self, host: str, port: int, router: Router, workers_count=os.cpu_count()):
        self.childrens_pull = []
        self.sock = None
        self.host = host
        self.port = port
        self.workers_count = workers_count

        self.router = router
        self.worker = Worker(router)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        log.print.info(f"Server is running on {self.host}:{self.port}")
        sock.listen()
        sock.setblocking(False)
        uvloop.install()
        self.worker.worker(sock)


class Worker:
    """
    Класс, работющий с непосредственно реквестами, необходим для дальнейшей модификации HTTPServer
    """

    def __init__(self, router: Router):
        self.router = router

    def worker(self, parent_sock: socket.socket):
        asyncio.run(self.__worker(parent_sock))

    async def __worker(self, parent_sock: socket.socket):
        while True:
            child_sock, _ = await asyncio.get_event_loop().sock_accept(parent_sock)
            await self.handle(child_sock)
            child_sock.close()

    async def handle(self, sock: socket.socket):
        raw = await asyncio.get_event_loop().sock_recv(sock, 1024)
        try:
            request = parse(raw)
        except Exception as e:
            log.print.error("Bad request with error: " + str(e))
            return
        if request is None:
            log.print.info("Served empty request")
            return
        log.print.info(request)
        try:
            result = await self.router.navigate(request)
            resp = result.get_answer()
        except Exception as e:
            resp = get_error(HTTP_INTERNAL_SERVER_ERROR, str(e))
        await asyncio.get_event_loop().sock_sendall(sock, resp.encode(ENCODING))
