from core import *
import core
import random
import atexit

atexit.register(stop)

global direction
while True:
    M.run(80)
    if black():  # hit black boundary
        b(1)
        spin('90')
        spin('90')

    if distance() <= 20:  # obstacle inbound
        direction = random.uniform(core._to_rolls('90'), core._to_rolls('90') * 2)
        if green():  # bonus
            M.run(65)
            while not hit():
                pass
            stop()
            sound()
            print("bonus !!!")
            b(1)  # go back
            direction = random.uniform(core._to_rolls('90'), core._to_rolls('90') * 2)
            spin(r=direction)
        else:
            b(1)
            direction = random.uniform(core._to_rolls('90'), core._to_rolls('90') * 2)
            spin(r=direction)