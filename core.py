# Copyright - Kiven, 2018

import nxt.locator as locator
from nxt.motor import *
from threading import Thread
from nxt.sensor import *
from time import sleep

gb_bound = 20  # todo: adapt these two values
gw_bound = 39

print("PyLego initializing.")
print("Copyright - Kiven, 2018")

b = None
L = None
R = None
lmove = Thread()
rmove = Thread()
M = SynchronizedMotors(None, None, None)
kill = False
light = None
sonic = None
touch = None


def reset(remote=False):
    global b, L, R, M, lmove, rmove, kill, light, sonic, touch
    print("Connecting")
    connect_method = locator.Method(not remote, remote)
    b = locator.find_one_brick(method=connect_method)
    print("Connection to brick established\n")

    print("Initializing sensors")
    L = m_left = Motor(b, PORT_B)
    R = m_right = Motor(b, PORT_C)
    M = SynchronizedMotors(L, R, 0.5)
    lmove = Thread()
    rmove = Thread()
    kill = False
    light = Light(b, PORT_3)
    sonic = Ultrasonic(b, PORT_2)
    touch = Touch(b, PORT_4)
    print("Initialization completed\n")
    print("Loading Actions")


if not b:
    try:
        reset()
    except:
        reset(True)

'''
def _handle_threads():
    def _do():
        global kill
        kill = True
        sleep(0.1)
        kill = False
    Thread(target=_do()).run()
'''

def l(r=1, p=75, t=None, b=True):  # changed the rule
    stop()
    if r < 15: # todo: say this in the documentation
        r *= 360
    L.turn(p, r, b)


def r(r=1, p=75, t=None, b=True):
    stop()
    if r < 15: # todo: say this in the documentation
        r *= 360
    R.turn(p, r, b)


right = r


def _l(r=1, p=100, t=None, b=True): # changed the rule
    if r < 15:  # todo: say this in the documentation
        r *= 360
    L.turn(p, r, b)


def _r(p=100, r=1, t=None, b=True):
    if r < 15:  # todo: say this in the documentation
        r *= 360
    R.turn(p, r, b)


def f(unlimited=False, r=1, p=100, t=None, b=True):
    global lmove, rmove, kill
    stop()
    if unlimited:
        M.run(p)
    else:
        M.turn(p, r if r >=15 else r*360, b)


def f(r=1, p=100, t=None, b=True):
    M.turn(p, r if r >= 15 else r * 360, b)


def b(unlimited=False, r=1, p=100, t=None, b=True):
    f(unlimited, -p, r, t, b)


def b(r=1, p=75, t=None, b=True):
    f(r, -p, t, b)


def _test():
    m = SynchronizedMotors(L, R, 0.5)
    m.turn(100, 360)


def stop():
    L.brake()
    R.brake()
    sleep(0.2)
    L.idle()
    R.idle()


def brightness():
    return light.get_lightness()


def distance():
    return sonic.get_distance()


def green():
    if gw_bound > brightness() > gb_bound:
        return True
    return False


def black():
    if brightness() < gb_bound:
        return True
    return False


def white():
    if brightness() > gw_bound:
        return True
    return False


def hit():
    return touch.is_pressed() or distance() < 5


def sound():
    Thread(target=b.play_tone_and_wait, args=(3, 1000)).start()
