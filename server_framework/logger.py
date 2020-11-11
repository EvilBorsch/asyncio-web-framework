import logging


class Logger:
    def __init__(self):
        l = logging.getLogger('main')
        # настраиваем логгинг
        l.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] [%(process)s] %(message)s',
            '%H:%M:%S'
        )
        ch.setFormatter(formatter)
        l.addHandler(ch)
        l.info('Run')
        self.print = l


log = Logger()
