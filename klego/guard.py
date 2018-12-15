from core import *
from time import sleep


def _guard():
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
        global _stop
        _stop = True
        stop()
        sleep(2)
        import sys
        sys.exit()

    def stopper():
        def work():
            global _stop
            _stop = True
            stop()
            sleep(5)
            _stop = False

        Thread(target=work).start()

    button1 = tk.Button(window, text='Stop Robot', command=stopper)
    button2 = tk.Button(window, text='Terminate Program', command=terminator)
    button1.pack()
    button2.pack()
    window.mainloop()


def guard_window():
    Thread(target=_guard).start()


def _test():
    _guard()
