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
from PID import *
from guard import *
# dev ops
_debug = True
_guard = False

# tunable parameters
GREEN_BLACK_BOUNDARY = 100  # deprecated
GREEN_WHITE_BOUNDARY = 250  # deprecated

TURN_RATIO = 1
LIGHT_BASE = 12
CM_EACH_ROLL = 0
LIGHT_SENSOR_ILLUMINATED = True

RADAR_BASE_INIT = 0.15
RADAR_BASE_PERIODIC = 0.3
RADAR_BASE_POWER = 100

# todo: test it out
_degree_to_seconds = to_secs = {

}
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


print("kLego initializing.")
print("Powered by Kiven - 2018\n")

# initializing protected fields and protected functions
# Protected fields and functions begin with '_',
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
color = None
dist = None
pos = Position()  # which marks the position of the robot
boxes = Boxes()  # which stores all the boxes here
pid = PID_Controller()

''' this file is to be run separately
'''


def _handle_radar_base(motor):
    motor.turn(RADAR_BASE_POWER, RADAR_BASE_INIT)

    def _run(motor):
        while True and not _stop:
            motor.turn(-RADAR_BASE_POWER, RADAR_BASE_PERIODIC)
            motor.turn(RADAR_BASE_POWER, RADAR_BASE_PERIODIC)

    Thread(target=_run, args=(motor,)).start()


def _get_counts(motor=None):
    if motor is None:
        motor = M
        return motor.get_tacho().leader_tacho.tacho_count, motor.get_tacho().follower_tacho.tacho_count
    return motor.get_tacho().tacho_count


def _wait():
    global _stop
    while _stop:
        sleep(0.001)


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


def _timed(func, t):
    pass


def to_cm(r):
    # this converts the roll param to centimeters
    if r > 15:  # todo: complete this
        r /= 360
    return r * CM_EACH_ROLL


def l(r=1, p=75, t=None, b=True):  # changed the rule
    sleep(0.2)
    if t:
        L.run(p)
        sleep(t)
        stop()
        return _get_counts(L) if _debug else None
    if r < 15:
        r *= 360
    L.turn(p, r, b)
    return _get_counts(L) if _debug else None


def r(r=1, p=75, t=None, b=True):
    sleep(0.2)
    if t:
        R.run(p)
        sleep(t), stop()
        return _get_counts(R) if _debug else None
    if r < 15:
        r *= 360
    R.turn(p, r, b)
    return _get_counts(R) if _debug else None


def spin(r=1.0, t=None, p=55):
    stop()
    # sleep(0.1)  # stabilize the motors
    global _lock
    if type(r) == str:
        pos.track(int(r), 0)
        r = to_rolls[r]
    if t:
        L.run(-p), R.run(p)
        sleep(t), stop()
        return _get_counts() if _debug else None

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

    if _debug:
        return _get_counts()


def hold_on():
    Thread(target=_locked(raw_input),
           args=("To end this hold-on, please enter anything: ",))\
        .start()
    global _lock
    while _lock:
        L.turn(1, 1)
        sleep(0.5)
        R.turn(1, 1)


def stopped(motor=None):
    if motor is None:
        motor = M
    return motor._get_new_state().power == 0


def power(single_motor):
    return single_motor._get_new_state().power


def _continuous_track():
    global M
    M.reset_position(True)
    prev, _ = _get_counts()
    while not stopped():
        sleep(0.05)
        # print("tracking")
        now, _ = 0, 0
        pos.track(0, to_cm(now-prev))
        prev = now


def _continuous_track_by_time(t, p):
    # todo: a dictionary mapping p (power) to short(intervals)
    dpm = 1

    def _run(t, p):
        while not stopped() and power(L) == power(R):  # still going straight
            sleep(0.1)
            pos.track(0, dpm)

    Thread(target=_run, args=(t, p)).start()


def f(r=1, t=None, p=75):
    global _lock
    # pos.track(0, to_cm(r))
    if t:
        M.run(p)
        sleep(t)
        M.brake()
        return _get_counts() if _debug else None
    if not r or r==0:  # unlimited
        M.run(p)
    else:
        M.turn(p, r if r >= 15 else r*360, False)
        M.brake()
    if _debug:
        return _get_counts() if _debug else None


def b(r=1, t=None, p=75):
    return f(r, t, -p)


def _test():
    m = SynchronizedMotors(L, R, 0.5)
    m.turn(100, 360)


def stop():
    global _stop
    _stop = True
    L.brake()
    R.brake()
    M.brake()
    sleep(0.2)
    L.idle()
    R.idle()
    M.idle()
    _stop = False


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


def reset(remote=False):
    global brick, L, R, M, radar_base, \
            light, sonic, touch, \
            LIGHT_BASE, _lock,\
            color, dist

    print "CORE: Connecting via", 'Bluetooth. May take up to 20 seconds' if remote else 'USB'
    connect_method = locator.Method(not remote, remote)
    brick = locator.find_one_brick(method=connect_method, debug=False)
    print("Connection to brick established\n")

    print("CORE: Initializing components")
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

    if _guard:
        guard_window()
    # calibrate light sensor
    light.set_illuminated(True)
    if not LIGHT_SENSOR_ILLUMINATED:
        light.set_illuminated(False)
    sleep(0.5)
    # _LIGHT_BASE_ = brightness() - 10
    print("Initialization completed\n")


try:
    reset()
except locator.BrickNotFoundError:
    print("CORE: USB connection not found. Switching connection to bluetooth\n")
    reset(True)

atexit.register(stop)
