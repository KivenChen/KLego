# in this file, special algorithms are applied to avoid
# failure detecting obstacle from the edge
from time import sleep
from threading import Thread
import numpy as np
import math

# sleep(1)
from core import going_back, going_forward, turning


_debug = False  # if broadcast debug info


def certain_history(hist):
    return hist.count(255) < 7


def update_dist(dist):
    # check if the reading change too rapidly
    history = dist.history
    now = history[:dist.IGNORE_MOST_RECENT]
    prev = history[dist.IGNORE_MOST_RECENT:]

    # algorithm: get the modes
    now = np.argmax(np.bincount(now))
    '''
    prev = np.argmax(np.bincount(prev))
    stable = abs(now - prev) < dist.EXCEPTION_THRESHOLD
    if stable and now > dist.NORMDIST_THRESHOLD:
        debug('safe', dist.now, dist.history)
    elif stable and now < dist.NORMDIST_THRESHOLD:
        dist.danger = True
        debug("too close to objects", dist.now, dist.history)
    elif not stable and now < dist.EXCPDIST_THRESHOLD:
        dist.danger = True
        debug("not stable", dist.now, dist.history)
    '''
    _r = Calc.time_linearity(history) if certain_history(history) else 1
    danger_dist = Calc.updated_danger_dist(
        dist.NORMDIST_THRESHOLD, _r, dist.algorithm)

    if now < danger_dist:
        dist.danger = True


def _monitor_dist(inst):
    sonic = inst.sensor
    print('DIST: initializing, may take 1 more second')
    sleep(1) 
    _prev_deta = 0
    print('DIST: ready')
    while True:
        sleep_interval = inst.INTERVAL - 0.01  # the sonic.get_distance method takes 0.01s to run
        if sleep_interval < 0:
            raise ValueError("the minimum of INTERVAL is 0.01 seconds")
        sleep(sleep_interval)

        # not responding to going_back because this cannot help
        if inst._lock:
            continue
        elif going_back() or turning():
            inst.danger = False
            continue
        inst.now = sonic.get_distance()

        # update history
        inst.history.pop()
        inst.history.insert(0, inst.now)
        update_dist(inst)


def debug(*args):
    if _debug:
        print "DIST: ", args


class Distance:
    _lock = False

    def activate(self):
        work = Thread(target=_monitor_dist, args=(self,), name='distance')
        work.start()

    def reset(self):
        self._lock = True
        sensor = self.sensor
        self.now = sensor.get_distance()
        self.history = [sensor.get_distance() for i in range(self.HISTORY_LEN)]
        self.states = ['safe' for i in range(self.HISTORY_LEN)]
        self._lock = False
        return self.history

    def __init__(self, sensor, obstacle_inbound=False):
        self.HISTORY_LEN = 10  # keep a history list of this length
        # self.HISTORY_ARCHIVE = 10 # length of the list where 1 in every 10 histories will be archived
        self.IGNORE_MOST_RECENT = 4  # a integer n. when compare the now to the prev, ignore the n most recent records
        self.INTERVAL = 0.1  # a float t which MUST BE > 0.01. Refresh distance every t seconds
        self.EXCEPTION_THRESHOLD = 90
        self.NORMDIST_THRESHOLD = 10
        self.EXCPDIST_THRESHOLD = 25

        self.states = ['safe' for i in range(self.HISTORY_LEN)]
        self.sensor = sensor
        self.now = sensor.get_distance()
        self.history = [sensor.get_distance() for i in range(self.HISTORY_LEN)]
        self.danger = obstacle_inbound
        self.algorithm = 'logistic'
        self.activate()

    def __call__(self):
        return self.now
        

class Calc:
    """encapsulates some calculation funcs"""

    @staticmethod
    def time_linearity(X):
        Y = [i for i in range(len(X))]
        raw = np.corrcoef(X, Y)
        result = abs(raw[0][1])
        return result if not np.isnan(result) else 0

    @staticmethod
    def sigmoid(x, logistic_coef):
        return 1 / (1 + np.exp((-x + 0.5)*logistic_coef))

    @staticmethod
    def updated_danger_dist(orig, linearity, algo='linear', logistic_coef=15):
        if algo == 'linear':
            return orig / linearity
        elif algo == 'sqrt':
            return orig / math.sqrt(linearity)
        elif algo == 'logistic':
            return Calc.sigmoid(linearity, logistic_coef)
