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
    color.activate = True
    while True and not _stop:
        if black():  # hit black boundary
            color.activate = False
            print('black')
            stop()
            b(1)
            color.activate = True
            color.color = 'white'
            color.reset()  # todo: if this is a green one?
            direction = random.uniform(core._to_rolls['90'], core._to_rolls['90'] * 2) // 0.01 / 100
            spin(direction)
            M.run(CRUISING_SPEED)

        if distance() <= 20 or touch.is_pressed() and not black():  # obstacle inboundd
            color.activate = False
            stop()
            print('obstacle inbound')
            M.run(APPROACHING_SPEED)  # slow down
            sleep(0.3)
            if green():  # bonus
                print("bonus !!!")
                sound()
                b(0.8)  # go back
                direction = random.uniform(core._to_rolls['90'], core._to_rolls['90'] * 2) // 0.01 / 100
                spin(direction)
                color.reset()
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

if __name__ == "__main__":
    test_parta()