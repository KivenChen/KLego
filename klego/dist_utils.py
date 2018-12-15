# in this file, special algorithms are applied to avoid
# failure detecting obstacle from the edge
from time import sleep
from threading import Thread

_debug = True  # if broadcast debug info


class Distance:
    _lock = False

    def debug(*args):
        if _debug:
            print "DIST: ", args

    def _monitor(self):
        sonic = self.sensor
        print('DIST: initializing, may take 1 more second')
        sleep(1)
        debug = self.debug

        while True:
            sleep_interval = self.INTERVAL - 0.01  # the sonic.get_distance method takes 0.01s to run
            if sleep_interval < 0:
                raise ValueError("the minimum of INTERVAL is 0.01 seconds")
            sleep(sleep_interval)
            if self._lock:
                continue
            self.now = sonic.get_distance()
            self.history.pop()
            self.history.insert(0, self.now)

            self.prev = sum(self.history[self.IGNORE_MOST_RECENT:]) / (self.HISTORY_LEN - self.IGNORE_MOST_RECENT)
            _delta = self.now - self.prev
            _threshold = 10

            if _delta > 100:  # approaching but not in an angle
                self.danger = True
                debug("great gap detected. Danger! ")
                _threshold = 200
                debug("threshold set to 200")
            elif self.now < _threshold:  # approaching and heading to target
                self.danger = True
                debug("facing object that is too close. Danger! ")
            elif self.danger and self.now > _threshold:
                self.danger = False
                debug("danger alert disarmed")
            self.reset()

    def activate(self):
        work = Thread(target=self._monitor, args=(self,))
        work.start()

    def reset(self):
        self._lock = True
        sensor = self.sensor
        self.now = sensor.get_distance()
        self.history = [sensor.get_distance() for i in range(self.HISTORY_LEN)]
        self._lock = False
        return self.history

    def __init__(self, sensor, obstacle_inbound=False):
        self.HISTORY_LEN = 10  # keep a history list of this length
        self.IGNORE_MOST_RECENT = 4  # a integer n. when compare the now to the prev, ignore the n most recent records
        self.INTERVAL = 0.02  # a float t which MUST BE > 0.01. Refresh distance every t seconds

        self.sensor = sensor
        self.now = sensor.get_distance()
        self.history = [sensor.get_distance() for i in range(self.HISTORY_LEN)]
        self.danger = obstacle_inbound
        self.activate()

    def __call__(self):
        return self.now
