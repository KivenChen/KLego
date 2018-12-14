from core import *
from core import spin as spin
import core
import random
import atexit
atexit.register(stop)

def test():
    M.run(80)
    sleep(1)
    b(1)

def run():
    while True:
        M.run(80)
        if black():  # hit black boundary
            b(1)
            spin('90')
            spin('90')

        if distance() <= 20:  # obstacle inbound
            M.run(65)
            if green() and False:  # bonus
                while not hit():
                    pass
                stop()
                print("bonus !!!")
                b(1)  # go back
                direction = random.uniform(core._to_rolls['90'], core._to_rolls['90'] * 3)
                direction = direction // 0.01 / 100
                spin(r=direction)
            else:
                b(1)
                stop()
                print("non-bonus, turning back")
                sleep(0.2)
                print("about to spin")
                # direction = random.uniform(core._to_rolls['90'], core._to_rolls['90'] * 3)
                # direction = direction // 0.01 / 100
                spin(0.9)
                print('spinned')

try:
    test()
except Exception as e:
    print(e.message)
finally:
    stop()