print 'guard utility: initializing'
from time import sleep
from threading import Thread
from random import randint
dist_label = None

def update_dist_data(dist_label):
    while True:
        sleep(0.005)
        text = str(randint(1,10)) + 'test'
        dist_label['text'] = text

def _guard(stop_func):
    global dist_label
    # to reduce dependency on tkinter
    # the module is not imported from the beginning
    try:
        from tkinter import Tk
        import tkinter as tk
    except ImportError:
        from TKinter import Tk
        import TKinter as tk

    window = Tk()
    window.title("kLego Guard")
    window.geometry("250x136")

    def terminator():
        stop_func()
        sleep(2)
        import sys
        sys.exit()




    def stopper():
        def work():
            stop_func()
            sleep(5)
        Thread(target=work).start()

    button1 = tk.Button(window, text='Stop Robot', command=stopper)
    button2 = tk.Button(window, text='Terminate Program', command=terminator)
    dist_label = tk.Label(window, text="ready")

    button1.pack()
    button2.pack()
    dist_label.pack()

    window.mainloop()


def guard_window(stop_func):
    Thread(target=_guard, args=(stop_func,)).start()


def _test():
    _guard()
