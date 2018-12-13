from core import *
from threading import *
from time import sleep
def syn():
    while True:
        sleep(1)
        print("here")
import atexit

atexit.register(stop)
Thread(target=syn).start()
M.run(-70)

sleep(5)
stop()