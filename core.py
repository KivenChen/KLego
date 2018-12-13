# Copyright - Kiven, 2018
from pos_utils import *
import nxt.locator as locator
from nxt.motor import *

from nxt.sensor import *
from time import sleep
from threading import Thread


_GREEN_BLACK_BOUNDARY_ = 20  # todo: adapt these two values
_GREEN_WHITE_BOUNDARY_ = 39

print("PyLego initializing.")
print("Copyright - Kiven, 2018")

# initializing fields.
# P.S. *private* fields and functions begin with '_',
# they are not supposed to be invoked by any users (for details please google or baidu it)
# and the author will not be responsible for any mistakes caused by this

brick = None
L = None
R = None
lmove = Thread()
rmove = Thread()
M = None
_lock = False
light = None
sonic = None
touch = None
guard_process = True
_debug = True
_TURN_RATIO_ = 1
_LIGHT_BASE_ = 0
pos = Position()  # which marks the position of the robot
boxes = Boxes()  # which stores all the boxes here


_degree_to_spin_r = _to_rolls = \
{
    '90': 0.7,
    '45': 0.33,
    '30': 0.22,
    '15': 0.11,
    '-90': -0.7,
    '-45': -0.35,
    '-30': -0.233,
}


def _guard():
    pass


def to_cm(r):
    # this converts the roll param to centimeters
    if r < 15:  # todo: complete this
        r *= 360
    pass




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


def _l(r=1, p=100, t=None, b=True):  # changed the rule
    if r < 15:  # todo: say this in the documentation
        r *= 360
    L.turn(p, r, b)


def _r(p=100, r=1, t=None, b=True):
    if r < 15:  # todo: say this in the documentation
        r *= 360
    R.turn(p, r, b)


def spin(r=1, p=75):
    sleep(0.2)
    global _lock
    if type(r) == str:
        pos.track(int(r), 0)
        r = _to_rolls[r]
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
    return L.get_tacho().tacho_count, R.get_tacho().tacho_count
    # print("exit turn")


def _locked(func):
    def output(*args):
        global _lock
        # print("locked")
        _lock = True
        func(*args)
        _lock = False
        # print("unlocked")
    return output


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


def _stopped(motor=None):
    if motor is None:
        motor = M
    return motor._get_new_state().power == 0


def _continuous_track():
    global M
    M.reset_position(True)
    prev, _ = _get_counts()
    while not _stopped():
        sleep(0.1)
        now, _ = _get_counts()
        pos.track(0, to_cm(now-prev))






def f(r=1, p=75, t=None):
    global _lock
    # pos.track(0, to_cm(r))
    if not r or r==0:  # unlimited
        M.run(p)
        Thread(target=_continuous_track()).start()
    else:
        M.turn(p, r if r >= 15 else r*360, False)
        M.brake()

    return M.get_tacho().leader_tacho.tacho_count, M.get_tacho().follower_tacho.tacho_count


def b(r=1, p=75, t=None):
    f(r, -p, t)


def _test():
    m = SynchronizedMotors(L, R, 0.5)
    m.turn(100, 360)


def stop():
    L.brake()
    R.brake()
    sleep(0.2)
    L.idle()
    R.idle()


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


def brightness():
    global _LIGHT_BASE_
    return light.get_lightness()-_LIGHT_BASE_


def distance():
    return sonic.get_distance()


def green():
    if _GREEN_WHITE_BOUNDARY_ > brightness() > _GREEN_BLACK_BOUNDARY_:
        return True
    return False


def black():
    if brightness() < _GREEN_BLACK_BOUNDARY_:
        return True
    return False


def white():
    if brightness() > _GREEN_WHITE_BOUNDARY_:
        return True
    return False


def hit():
    return touch.is_pressed() or distance() < 5


def sound():
    Thread(target=brick.play_tone_and_wait, args=(3, 1000)).start()

def reset(remote=False):
    global brick, L, R, M, lmove, rmove, _lock, light, sonic, touch
    try:
        locator.read_config()
    except:
        locator.make_config()
    print("Connecting")
    connect_method = locator.Method(not remote, remote)
    brick = locator.find_one_brick(method=connect_method, debug=True)
    print("Connection to brick established\n")

    print("Initializing sensors")
    L = Motor(brick, PORT_B)
    R = Motor(brick, PORT_C)
    L.get_tacho()
    M = SynchronizedMotors(L, R, _TURN_RATIO_)
    lmove = Thread()
    rmove = Thread()
    _lock = False
    light = Light(brick, PORT_3)
    sonic = Ultrasonic(brick, PORT_2)
    touch = Touch(brick, PORT_4)

    # calibrate light sensor
    light.set_illuminated(True)
    light.set_illuminated(False)
    sleep(0.5)
    _LIGHT_BASE_ = brightness()
    print("Initialization completed\n")

reset(False)

