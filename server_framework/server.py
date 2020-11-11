import asyncio
import atexit
import multiprocessing as mp
import os
import socket

import uvloop

from server_framework.answer_codes import HTTP_OK
from server_framework.logger import log
from server_framework.parser import parse, Response, Request, ENCODING
from server_framework.router import Router


class MainServer:
    def __init__(self, host: str, port: int, router: Router, workers_count=os.cpu_count()):
        self.childrens_pull = []
        self.sock = None
        self.host = host
        self.port = port
        self.workers_count = workers_count
        self.router = router

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
        p = mp.Process(target=worker, args=(parent_sock,))
        p.start()
        self.childrens_pull.append(p)

    def kill_children(self):
        for c in self.childrens_pull:
            c.terminate()
            c.join()


def worker(parent_sock: socket.socket):
    asyncio.run(__worker(parent_sock))


async def __worker(parent_sock: socket.socket):
    while True:
        child_sock, _ = await asyncio.get_event_loop().sock_accept(parent_sock)
        await handle(child_sock)
        child_sock.close()


async def handle(sock: socket.socket):
    raw = await asyncio.get_event_loop().sock_recv(sock, 1024)
    request = parse(raw)
    if request is None:
        log.print.info('Served empty request')
        return

    log.print.info(request)
    handler_response = await test_handler(request)
    resp = handler_response.get_answer()
    await asyncio.get_event_loop().sock_sendall(sock, resp.encode(ENCODING))


async def test_handler(req: Request) -> Response:
    return Response(status=HTTP_OK, data="""{"kek":2}""")
