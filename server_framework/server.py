import asyncio
import atexit
import multiprocessing as mp
import os
import socket

import uvloop

from server_framework.answer_codes import HTTP_INTERNAL_SERVER_ERROR
from server_framework.logger import log
from server_framework.parser import parse, ENCODING, get_error
from server_framework.router import Router


class MainServer:
    def __init__(self, host: str, port: int, router: Router, workers_count=os.cpu_count()):
        self.childrens_pull = []
        self.sock = None
        self.host = host
        self.port = port
        self.workers_count = workers_count
        self.router = router
        self.worker = Worker(router)  # this need to bind worker to process
        self.worker.router.routes = router.routes

        atexit.register(self.kill_children)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        log.print.info(f'Server is running on {self.host}:{self.port}')
        sock.listen()
        sock.setblocking(False)

        uvloop.install()

        for i in range(self.workers_count):
            self.prefork(sock)

        try:
            for worker in self.childrens_pull:
                worker.join()
        except KeyboardInterrupt:
            for worker in self.childrens_pull:
                worker.terminate()
            sock.close()
            log.print.info('Server was manually stopped')

    def prefork(self, parent_sock: socket.socket):
        p = mp.Process(target=self.worker.worker, args=(parent_sock,))
        p.start()
        self.childrens_pull.append(p)

    def kill_children(self):
        for c in self.childrens_pull:
            c.terminate()
            c.join()


class Worker:
    def __init__(self, router: Router):
        self.router = router
        print(self.router)

    def worker(self, parent_sock: socket.socket):
        asyncio.run(self.__worker(parent_sock))

    async def __worker(self, parent_sock: socket.socket):
        while True:
            child_sock, _ = await asyncio.get_event_loop().sock_accept(parent_sock)
            await self.handle(child_sock)
            child_sock.close()

    async def handle(self, sock: socket.socket):
        raw = await asyncio.get_event_loop().sock_recv(sock, 1024)
        request = parse(raw)
        if request is None:
            log.print.info('Served empty request')
            return
        log.print.info(request)
        try:
            result = await self.router.navigate(request)
            resp = result.get_answer()
        except Exception as e:
            resp = get_error(HTTP_INTERNAL_SERVER_ERROR, str(e))
        await asyncio.get_event_loop().sock_sendall(sock, resp.encode(ENCODING))
