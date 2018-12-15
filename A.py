from core import *
import core
import random
import atexit

from tkinter import Tk
import tkinter as tk
from sys import exit

atexit.register(stop)

# tunable parameters
CRUISING_SPEED = 75
APPROACHING_SPEED = 55



def test():
    M.run(CRUISING_SPEED)
    sleep(1)
    b(1)


def run():
    M.idle()
    M.reset_position(False)
    M.run(CRUISING_SPEED)
    color.activate = True
    while True and not _stop:
        if black():  # hit black boundary
            # color.activate = False
            print('black')
            stop()
            b(1, p=120)
            color.activate = True
            color.color = 'white'
            color.reset()  # todo: if this is a green one?
            direction = random.uniform(core.to_rolls['90'], core.to_rolls['90'] * 1.5) // 0.01 / 100
            spin(direction)
            M.run(CRUISING_SPEED)

        if distance() <= 30 or touch.is_pressed() or green():  # obstacle inboundd
            stop()
            print('obstacle inbound')
            M.run(APPROACHING_SPEED)  # slow down
            sleep(0.2)
            if green():  # bonus
                print("bonus !!!")
                stop()
                f(0.3)
                sound()
                b(1)  # go back
                stop()
                direction = random.uniform(core.to_rolls['45'], core.to_rolls['90'] * 2) // 0.01 / 100
                spin(direction)
                color.reset()
                M.run(CRUISING_SPEED)
            else:
                print('danger: non bonus obstacle')
                b(0.5, p=120)
                stop()
                print("non-bonus, turning back")
                print("about to spin")
                direction = random.uniform(core.to_rolls['45'], core.to_rolls['90'] * 2) // 0.01 / 100
                spin(direction)
                print('spinned')
                M.run(CRUISING_SPEED)
            color.activate = True


def test_parta():
    try:
        print('guard: in progress')
        get_guard().start()
        run()
    except Exception as e:
        print(e.message)
    finally:
        stop()


def watcher():
    # watch the obstacle inbound
    pass


if __name__ == "__main__":
    test_parta()
