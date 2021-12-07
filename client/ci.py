import time

INITIAL_INTERVAL = 1
MIN_INTERVAL = 0.0125
DEC_RATIO = 0.8


class ControlInterval(object):

    def __init__(self) -> None:
        self.prev_time = None
        self.interval = INITIAL_INTERVAL

    def check_interval(self) -> None:
        if self.prev_time is None:
            self.prev_time = time.time()
            return

        if self.prev_time - time.time() < INITIAL_INTERVAL:
            time.sleep(self.interval)
            if self.interval > MIN_INTERVAL:
                self.interval = self.interval * DEC_RATIO
