# Copyright - Kiven, 2018
from pos_utils import *
import nxt.locator as locator
from nxt.motor import *
import atexit
from nxt.sensor import *
from time import sleep
from threading import Thread
from color_utils import *
from dist_utils import *
import tkinter as tk
from tkinter import Tk


# tunable parameters
GREEN_BLACK_BOUNDARY = 100  # deprecated
GREEN_WHITE_BOUNDARY = 250
_debug = True
TURN_RATIO = 1
LIGHT_BASE = 12
CM_EACH_ROLL = 0
_illuminate = True
RADAR_BASE_INIT = 0.15
RADAR_BASE_PERIODIC = 0.3
RADAR_BASE_POWER = 100

_degree_to_spin_r = to_rolls = \
{
    '90': 0.51,
    '45': 0.26,
    '30': 0.11,
    '15': 0.085,
    '-90': -0.52,
    '-45': -0.265,
    '-30': -0.173,
    '-15': -0.086,
}

def gw(val):  # deprecated
    global GREEN_WHITE_BOUNDARY
    GREEN_WHITE_BOUNDARY = val


def gb(val):  # deprecated
    global GREEN_BLACK_BOUNDARY
    GREEN_BLACK_BOUNDARY = val

print("PyLego initializing.")
print("Copyright - Kiven, 2018")

# initializing fields.
# P.S. *private* fields and functions begin with '_',
# they are not supposed to be invoked by any users (for details please google or baidu it)
# and the author will not be responsible for any mistakes caused by this

brick = None
L = None
R = None
M = None
Radar = None
_lock = False
_stop = False
light = None
sonic = None
touch = None
guard_process = True
color = None
dist = None
pos = Position()  # which marks the position of the robot
boxes = Boxes()  # which stores all the boxes here


''' this file is to be run separately
'''

from tkinter import Tk
import tkinter as tk


def _guard():
    window = Tk()
    def exiter():
        global _stop
        _stop = True
        stop()
        sleep(2)
        import sys
        sys.exit()

    def stopper():
        global _stop

        def work():
            _stop = True
            stop()
            sleep(5)
            _stop = False

        Thread(target=work).start()

    button1 = tk.Button(window, text='stop', command=stopper)
    button2 = tk.Button(window, text='terminate', command=exiter)
    button1.pack()
    button2.pack()
    window.mainloop()


def get_guard():
    return Thread(target=_guard)


def to_cm(r):
    # this converts the roll param to centimeters
    if r > 15:  # todo: complete this
        r /= 360
    return r * CM_EACH_ROLL




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
    sleep(0.2)
    if r < 15:
        r *= 360
    L.turn(p, r, b)


def r(r=1, p=75, t=None, b=True):
    sleep(0.2)
    if r < 15:
        r *= 360
    R.turn(p, r, b)


right = r


def _l(r=1.0, p=100, t=None, b=True):  # changed the rule
    if r < 15:  # todo: say this in the documentation
        r *= 360
    L.turn(p, r, b)


def _r(p=100, r=1, t=None, b=True):
    if r < 15:  # todo: say this in the documentation
        r *= 360
    R.turn(p, r, b)


def _locked(func):
    def output(*args):
        global _lock
        # print("locked")
        _lock = True
        try:
            func(*args)
        except Exception as e:
            print e.message
        finally:
            _lock = False
        # print("unlocked")
    return output


def spin(r=1.0, p=55):
    # L.reset_position(True)
    # R.reset_position(True)
    stop()
    # M.idle()
    sleep(0.1)
    global _lock
    if type(r) == str:
        pos.track(int(r), 0)
        r = to_rolls[r]
    if r < 0:
        r, p = -r, -p
    if r < 15:
        r = int(360*r)  # considered that the _to_roll returns float
    op1 = Thread(target=_locked(L.turn), args=(-p, r, False))
    op2 = Thread(target=_locked(R.turn), args=(p, r, False))
    op1.start()
    op2.start()
    while _lock:
        pass
    stop()
    return L.get_tacho().tacho_count, R.get_tacho().tacho_count
    # print("exit turn")


def hold_on():
    Thread(target=_locked(raw_input),
           args=("To end this hold-on, please enter anything: ",))\
        .start()
    global _lock
    while _lock:
        L.turn(1, 1)
        sleep(0.5)
        R.turn(1, 1)


def _get_counts(motor=None):
    if motor is None:
        motor = M
        return motor.get_tacho().leader_tacho.tacho_count, motor.get_tacho().follower_tacho.tacho_count
    return motor.get_tacho().tacho_count


_temp = 0


def stopped(motor=None):
    if motor is None:
        motor = M
    return motor._get_new_state().power == 0


def _continuous_track():
    global M
    M.reset_position(True)
    prev, _ = _get_counts()
    while not stopped():
        sleep(0.1)
        # print("tracking")
        now, _ = 0, 0
        pos.track(0, to_cm(now-prev))
        prev = now


def f(r=1, p=75, t=None):
    global _lock
    # pos.track(0, to_cm(r))
    if not r or r==0:  # unlimited
        M.run(p)
    else:
        M.turn(p, r if r >= 15 else r*360, False)
        M.brake()
    # return M.get_tacho().leader_tacho.tacho_count, M.get_tacho().follower_tacho.tacho_count


def b(r=1, p=75, t=None):
    f(r, -p, t)


def _test():
    m = SynchronizedMotors(L, R, 0.5)
    m.turn(100, 360)


def stop():
    L.brake()
    R.brake()
    M.brake()
    sleep(0.2)
    L.idle()
    R.idle()
    M.idle()


def _discover(boxes, pos, sonic_dist):
    # this method records a new block
    # if this one is an existed one, return false
    _DELTA_ = 0
    if sonic_dist > 200:
        return False
    robo_pos = pos
    x = robo_pos.x
    y = robo_pos.y
    d = robo_pos.d
    dx = int(sin(rad(d)) * float(sonic_dist))
    dy = int(cos(rad(d)) * float(sonic_dist))
    t_x = x + dx
    t_y = y + dy
    pos = Position(t_x, t_y)
    if boxes.overlapped(pos):
        return False
    else:
        boxes.add(pos)
        return True


def discover(boxes):
    # automatically rotate 360 and record every boxes detected within 200 cm
    global pos
    for i in range(12):
        _discover(boxes, pos, distance())
        spin('30')


def brightness():  # for Task-A this is deprecated, use color() instead
    global LIGHT_BASE
    return light.get_lightness() - LIGHT_BASE


def distance():
    return dist.now


def green():  # this one needs verification
    if color('green'):
        sleep(0.2)
    return color('green')


def black():
    return color('black')


def white():
    return color('white')


def hit():
    return touch.is_pressed() or distance() < 5


def calibrate_light_by_black():  # deprecated
    global LIGHT_BASE
    LIGHT_BASE = light.get_lightness() - 10


def sound():
    Thread(target=brick.play_tone_and_wait, args=(1000, 500)).start()


def _handle_radar_base(motor):
    motor.turn(RADAR_BASE_POWER, RADAR_BASE_INIT)

    def _run(motor):
        while True and not _stop:
            motor.turn(-RADAR_BASE_POWER, RADAR_BASE_PERIODIC)
            motor.turn(RADAR_BASE_POWER, RADAR_BASE_PERIODIC)

    Thread(target=_run, args=(motor,)).start()


def reset(remote=False):
    global brick, L, R, M, radar_base, \
            light, sonic, touch, \
            LIGHT_BASE, _lock,\
            color, dist

    print("CORE: Connecting")
    connect_method = locator.Method(not remote, remote)
    brick = locator.find_one_brick(method=connect_method, debug=True)
    print("Connection to brick established\n")

    print("CORE: Initializing componentss")
    L = Motor(brick, PORT_B)
    R = Motor(brick, PORT_C)
    M = SynchronizedMotors(L, R, TURN_RATIO)

    try:
        radar_base = Motor(brick, PORT_A)
        print("CORE: Found radar turning base")
        _handle_radar_base(radar_base)
    except:
        print("CORE: Found no radar turning base connecting PORT A")
        print("Normal Mode activated")

    _lock = False
    light = Light(brick, PORT_3)
    sonic = Ultrasonic(brick, PORT_2)
    touch = Touch(brick, PORT_4)
    color = Color(light)
    global dist
    dist = Distance(sonic)

    # calibrate light sensor
    light.set_illuminated(True)
    if not _illuminate:
        light.set_illuminated(False)
    sleep(0.5)
    # _LIGHT_BASE_ = brightness() - 10
    print("Initialization completed\n")


try:
    reset()
except locator.BrickNotFoundError:
    print("\nCORE: USB connection not found. Switching connection to bluetooth \n")
    reset(True)

atexit.register(stop)

