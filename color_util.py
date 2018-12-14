'''to eliminate the problem of light problem,
I decided to monitor the light
instead of using a fix value to classif'''

_debug_global = False
_debug_color = True
_power_ref = 0

from threading import Thread
from time import sleep
B_TO_G = 20
G_TO_W = 15
B_TO_W = B_TO_G + G_TO_W


def _handle_green_saparately(self):
    if self.color == 'green':
        pass


def _monitor(self):
    print("COLOR: initializing, 1 second to wait")
    sleep(1)  # well ... I'm pretty sure only ONE sec is needed actually
    from core import L, R
    light = self.sensor
    while True:
        _power = max((abs(L._get_new_state().power), abs(R._get_new_state().power)))
        _r = 1
        if _power < 50:  # not even moving
            continue
        sleep(0.05)

        _handle_green_saparately(self)
        self.history.pop()
        self.history.insert(0, self.now)
        self.prev = sum(self.history) / 10
        self.now = light.get_lightness()
        if _debug_color and abs(self.prev - self.now) > 10:
            print "COLOR value change: ", self.prev, ' to ', self.now, ', now', self.color.upper()
        # GETTING BRIGHTER
        if _r*B_TO_G > self.now - self.prev > _r*G_TO_W:
            if self.color == 'green':
                self.color = 'white'
                print("COLOR: change from GREEN 2 WHITE")
        elif _r*B_TO_G < self.now- self.prev < _r*B_TO_W and self.color == 'black':
                self.color = 'green'
                print("COLOR: change from BLACK 2 GREEN")
        elif _r*B_TO_W < self.now - self.prev and self.color == 'black':
            self.color = 'white'
            print("COLOR: change from BLACK 2 WHITE")

        # GETTING DARKER
        if _r*B_TO_G > self.prev - self.now > G_TO_W*_r:
            if self.color == 'white':
                self.color = 'green'
                print("COLOR: change from WHITE 2 GREEN")
        elif _r*B_TO_G < self.prev - self.now < _r*B_TO_W:
            if self.color == 'green':
                self.color = 'black'
                print("COLOR: change from GREEN 2 BLACK")
        elif _r*B_TO_W < self.prev - self.now:
            if self.color == 'white':
                self.color = 'black'
                print("COLOR: change from WHITE 2 BLACK")


class Color:
    def __init__(self, sensor, calibrate_by='white'):
        self.sensor = sensor
        self.history = [sensor.get_lightness() for i in range(10)]
        self.now = sensor.get_lightness()
        self.color = calibrate_by
        work = Thread(target=_monitor, args=(self,))
        work.start()

    def __call__(self, *args, **kwargs):
        if args != ():
            return any([i == self.color for i in args])
        return self.color
