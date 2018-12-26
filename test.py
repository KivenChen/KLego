from matplotlib import pyplot as plt
import numpy as np
from threading import Thread
from time import sleep
from random import uniform


class DistDebugger:
    # provide pyplot window for debug
    def __init__(self, archived_hist, fig_num=1):
        self.archived_hist = archived_hist
        self.fig = plt.figure(fig_num)
        self.plot = self.fig.add_subplot(1, 1, 1)

    def update(self):
        time_seq = range(len(self.archived_hist))
        self.plot.clear()
        self.plot.scatter(time_seq, self.archived_hist)

    @staticmethod
    def avoid_suspension():
        plt.pause(0.1)


history = []
window = DistDebugger(history)
for i in range(200):
    if len(history) > 200:
        history.pop()
    history.insert(0, uniform(-1, 1))
    window.avoid_suspension()
    sleep(0.1)
    window.update()




