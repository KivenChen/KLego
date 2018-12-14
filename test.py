from core import *
from threading import *
from time import sleep
import tkinter as tk
from tkinter import Tk

def syn():
    while True:
        sleep(1)
        print("here")
import atexit

def guard():
    window = Tk()
    def com():
        global _stop
        _stop = True
        stop()
        exit()
    button = tk.Button(window, text='stop', command=com)
    button.pack()
    window.mainloop()

atexit.register(stop)
