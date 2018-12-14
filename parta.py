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
CRUISING_SPEED = 70
APPROACHING_SPEED = 55



def test():
    M.run(CRUISING_SPEED)
    sleep(1)
    b(1)


def run():
    M.idle()
    M.reset_position(False)
    M.run(CRUISING_SPEED)
    while True and not _stop:
        if black():  # hit black boundary
            print('black')
            stop()
            b(1)
            spin('90')
            M.run(CRUISING_SPEED)

        if distance() <= 25 or green() and not black():  # obstacle inbound
            stop()
            print('obstacle inbound')
            M.run(APPROACHING_SPEED)  # slow down
            if green():  # bonus
                print("bonus !!!")
                sound()
                b(0.5)  # go back
                direction = random.uniform(core._to_rolls['45'], core._to_rolls['90'] * 2) // 0.01 / 100
                spin(direction*1.5)
                M.run(CRUISING_SPEED)
            else:
                print('non bonus')
                b(0.5, p=120)
                print("non-bonus, turning back")
                print("about to spin")
                direction = random.uniform(core._to_rolls['45'], core._to_rolls['90'] * 2) // 0.01 / 100
                spin(direction)
                print('spinned')
                M.run(CRUISING_SPEED)


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