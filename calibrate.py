from core import *
from threading import Thread
import tkinter as tk

window = None

def gui():
    global window
    main = tk.Tk()
    slide_alpha = tk.Scale(main, from_=0, to=40)
    slide_alpha.pack()
    slide_beta = tk.Scale(main, from_=0, to=40)



def calibrate_task_b():
    # this method will create the thread to adjust
    pass


def dark():
    if black():
        return True
    return False


def handle_turn():
    # this method will start the thread to execute Task-B
    if green() or dark():
        r(150)
        pass  # turn right
    else:  # sensing light
        l(150)
        pass # turn left
    handle_turn()


def blackline():
    f(0)
    while dark():
        pass
    handle_turn()


def guard():
    a = raw_input()
    stop()
    print('stopped')
    while True:
        drv = raw_input()
        eval(drv)

Thread(target=guard).start()
sleep()
blackline()
