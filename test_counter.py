import time


class Test:
    def __init__(self, cb):
        self.is_running = 0
        self.status = "Inited"
        self._cb = cb

    def run(self):
        self.is_running = 1
        for i in range(100):
            self.status = f'{i}'
            print(self.status)
            self._cb(self.status)
            time.sleep(1)
        self.is_running = 0
