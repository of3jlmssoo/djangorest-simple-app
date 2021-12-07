import time


class ControlInterval(object):
    def __init__(self) -> None:
        self.prev_time = None
        self.interval = 1

    def check_interval(self):
        if self.prev_time is None:
            self.prev_time = time.time()
            return

        if self.prev_time - time.time() < 1:
            time.sleep(self.interval)
            if self.interval > 0.0125:
                self.interval = self.interval * 0.8
