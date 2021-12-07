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


controlinterval = ControlInterval()
for i in range(30):
    controlinterval.check_interval()
    print(f'{i} message')

controlinterval2 = ControlInterval()
for c in list('------------ end of the message ------------'):
    controlinterval2.check_interval()
    print(c, end='', flush=True)
