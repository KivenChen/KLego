from core import *
from core import spin as spin
import core
import random
import atexit
from tkinter import Tk
import tkinter as tk
from sys import exit
from core import _stop

atexit.register(stop)

def test():
    M.run(80)
    sleep(1)
    b(1)

def run():
    M.idle()
    M.reset_position(False)
    M.run(80)
    while True and not _stop:
        if black():  # hit black boundary
            print('black')
            stop()
            r(1.5)

        if distance() <= 19 or green() and not black():  # obstacle inbound
            print('distance or green')
            M.run(65)  # slow down
            print('slowed down')
            if green():  # bonus
                while not hit():
                    pass
                print("bonus !!!")
                b(0.5)  # go back
                direction = random.uniform(core._to_rolls['90'], core._to_rolls['90'] * 3) // 0.01 / 100
                r(direction*1.5)
                M.run(80)
            else:
                print('non bonus')
                b(0.5, p=120)
                print("non-bonus, turning back")
                print("about to spin")
                direction = random.uniform(core._to_rolls['90'], core._to_rolls['90'] * 3) // 0.01 / 100
                r(1.5)
                print('spinned')
                M.run(80)


def test_parta():
    try:
        print('guard: in progress')
        get_guard().start()
        run()
    except Exception as e:
        print(e.message)
    finally:
        stop()

if __name__ == "__main__":
    test_parta()