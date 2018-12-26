# in this file, special algorithms are applied to avoid
# failure detecting obstacle from the edge
from time import sleep
from threading import Thread
import numpy as np
import math
from matplotlib import pyplot as plt


alarmed = False
# sleep(1)
from core import going_back, going_forward, turning


_debug = False  # if broadcast debug info
_debug_window = True  # if show debug window


def stable_history(hist):
    return np.all(np.bincount(hist) < 6)


def update_dist(dist):
    global alarmed
    # check if the reading change too rapidly
    history = dist.history
    now = history[:dist.IGNORE_MOST_RECENT]
    prev = history[dist.IGNORE_MOST_RECENT: dist.HISTORY_LEN]
    # algorithm: get the modes
    now_dist = np.argmax(np.bincount(now))
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
    if stable_history(history[:dist.HISTORY_LEN]):
        _r = Calc.time_linearity(history[:dist.HISTORY_LEN])
        is_static = True
        prev = None
        for i in now[1:]:
            if i != prev or not prev:
                is_static = False
                break
            prev = i
        if not is_static:
            dist.danger_dist = Calc.updated_danger_dist(
                dist.NORMDIST_THRESHOLD, _r, dist.algorithm)
    else:
        # print "unstable history: not updating"
        pass
    if now_dist < dist.danger_dist:
        dist.danger = True
        if not alarmed:
            print "DIST: DANGER - threshold", dist.danger_dist, dist.history, dist.now
            alarmed = True


def _monitor_dist(inst):
    global alarmed
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
            inst.danger_dist = 5
            alarmed = False
            inst.history = []
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

    def _monitor_dist(self):
        sonic = self.sensor
        print('DIST: initializing, may take 1 more second')
        sleep(1)
        _prev_deta = 0
        print('DIST: ready')
        while True:
            danger_dist = self.NORMDIST_THRESHOLD
            sleep_interval = self.INTERVAL - 0.01  # the sonic.get_distance method takes 0.01s to run
            if sleep_interval < 0:
                raise ValueError("the minimum of INTERVAL is 0.01 seconds")
            sleep(sleep_interval)

            # not responding to going_back because this cannot help
            if self._lock:
                continue
            elif going_back() or turning():
                self.danger = False
                continue
            self.now = sonic.get_distance()

            # update history
            self.history.pop()
            self.history.insert(0, self.now)
            self.update_dist()

    def update_dist(self):
        # check if the reading change too rapidly
        history = self.history
        now = history[:self.IGNORE_MOST_RECENT]
        prev = history[self.IGNORE_MOST_RECENT:]

        # algorithm: get the modes
        now = np.argmax(np.bincount(now))

        if self.debug_win:
            self.archived_history.append(now)
            if len(self.archived_history) > self.ARCHIVE_HIST_LEN:
                self.archived_history.pop(1)
            self.debug_win.archived_hist = self.archived_history
            self.debug_win.update()
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
        '''
        _r = Calc.time_linearity(history) if certain_history(history) else 1
        danger_dist = Calc.updated_danger_dist(
            self.NORMDIST_THRESHOLD, _r, self.algorithm)
        '''
        danger_dist = self.NORMDIST_THRESHOLD
        if now < danger_dist:
            self.danger = True

    def activate(self):
        work = Thread(target=self._monitor_dist, name='distance')
        work.start()

    def reset(self):
        self._lock = True
        sensor = self.sensor
        self.now = sensor.get_distance()
        self.history = [sensor.get_distance() for i in range(self.HISTORY_LEN)]
        self.states = ['safe' for i in range(self.HISTORY_LEN)]
        self._lock = False
        return self.history

    def _plotting(self):
        pass

    def __init__(self, sensor, obstacle_inbound=False):
        self.HISTORY_LEN = 10  # keep a history list of this length
        # self.HISTORY_ARCHIVE = 10 # length of the list where 1 in every 10 histories will be archived
        self.IGNORE_MOST_RECENT = 4  # a integer n. when compare the now to the prev, ignore the n most recent records

        self.INTERVAL = 0.05  # a float t which MUST BE > 0.01. Refresh distance every t seconds
        self.EXCEPTION_THRESHOLD = 90
        self.NORMDIST_THRESHOLD = 25
        self.EXCPDIST_THRESHOLD = 25
        self.ARCHIVE_HIST_LEN = 200

        self.INTERVAL = 0.07  # a float t which MUST BE > 0.01. Refresh distance every t seconds
        self.EXCEPTION_THRESHOLD = 90
        self.NORMDIST_THRESHOLD = 5
        self.danger_dist = 5

        self.sensor = sensor
        self.now = sensor.get_distance()

        self.history = [sensor.get_distance() for i in range(self.HISTORY_LEN)]
        self.archived_history = [0, 0]

        self.history = [sensor.get_distance() for i in range(self.HISTORY_LEN * 2)]

        self.danger = obstacle_inbound
        self.algorithm = 'linear'
        self.activate()
        self.debug_win = None
        if _debug_window:
            self.debug_win = DistDebugger(self.archived_history, self.INTERVAL)

    def __call__(self):
        return self.now
        

class Calc:
    """encapsulates some calculation funcs"""
    @staticmethod
    def time_linearity(X):
        Y = [i for i in range(len(X))]
        raw = np.corrcoef(X, Y)
        result = np.clip(raw[0][1], 0.01, 1)
        return result if not np.isnan(result) and not result < 0.01 else 0.04

    @staticmethod
    def sigmoid(x, logistic_coef):
        return 1 / (1 + np.exp((-x + 0.5)*logistic_coef))

    @staticmethod
    def updated_danger_dist(orig, linearity, algo='linear', logistic_coef=5):
        if algo == 'linear':
            return orig / linearity
        elif algo == 'sqrt':
            return orig / math.sqrt(linearity)
        elif algo == 'logistic':
            return Calc.sigmoid(linearity, logistic_coef)


class DistDebugger:
    # provide pyplot window for debug
    def __init__(self, archived_hist, interval):
        self.archived_hist = archived_hist
        self.fig = plt.figure()
        self.plot = self.fig.add_subplot(1, 1, 1)
        self.interval = interval

    def update(self):
        self.plot.clear()
        time_seq = [i for i in range(len(self.archived_hist))]
        self.plot.scatter(time_seq, self.archived_hist)
        self._avoid_suspension()

    def _avoid_suspension(self):
        # plt.pause(self.interval)
        pass

