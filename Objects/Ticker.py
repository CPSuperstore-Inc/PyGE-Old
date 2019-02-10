from time import time


class Ticker:
    def __init__(self):
        self.last = time()

    @property
    def tick(self):
        delta = time() - self.last
        self.last = time()
        return delta
