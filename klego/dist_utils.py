# in this file, special algorithms are applied to avoid
# failure detecting obstacle from the edge
from time import sleep
from threading import Thread

_debug = True  # if broadcast debug info


def _monitor(inst):
    sonic = inst.sensor
    print('DIST: initializing, may take 1 more second')
    sleep(1)
    print('DIST: ready')
    while True:
        sleep_interval = inst.INTERVAL - 0.01  # the sonic.get_distance method takes 0.01s to run
        if sleep_interval < 0:
            raise ValueError("the minimum of INTERVAL is 0.01 seconds")
        sleep(sleep_interval)
        if inst._lock:
            continue
        inst.now = sonic.get_distance()
        inst.history.pop()
        inst.history.insert(0, inst.now)

        inst.prev = sum(inst.history[inst.IGNORE_MOST_RECENT:]) / (inst.HISTORY_LEN - inst.IGNORE_MOST_RECENT)
        _delta = inst.now - inst.prev
        _threshold = 10

        if _delta > 100:  # approaching but not in an angle
            inst.danger = True
            debug("great gap detected. Danger! ")
            _threshold = 200
            debug("threshold set to 200")
        elif inst.now < _threshold:  # approaching and heading to target
            inst.danger = True
            debug("facing object that is too close. Danger! ")
        elif inst.danger and inst.now > _threshold:
            inst.danger = False
            debug("danger alert disarmed")
        inst.reset()


def debug(*args):
    if _debug:
        print "DIST: ", args


class Distance:
    _lock = False

    def activate(self):
        work = Thread(target=_monitor, name='distance')
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
