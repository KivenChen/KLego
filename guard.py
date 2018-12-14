''' this file is to be run separately
'''
from tkinter import Tk
import tkinter as tk
from core import *

def guard():
    window = Tk()
    def exiter():
        global _stop
        _stop = True
        stop()
        import sys
        sys.exit()
    def stopper():
        global _stop
        _stop = True
        stop()
        _stop = False
    button = tk.Button(window, text='stop', command=exiter)
    button = tk.Button(window, text='terminate', command=stopper())
    button.pack()
    window.mainloop()
