'''to eliminate the problem of light problem,
I decided to monitor the light
instead of using a fix value to classif'''

_debug_global = False
_debug_color = True
_power_ref = 0

from threading import Thread
from time import sleep
B_TO_G = 40
G_TO_W = 15
B_TO_W = B_TO_G + G_TO_W


def _monitor(self):
    print("COLOR: initializing, 1 second to wait")
    sleep(1)  # well ... I'm pretty sure only ONE sec is needed actually
    from core import L, R
    light = self.sensor
    while True:
        _power = max((abs(L._get_new_state().power), abs(R._get_new_state().power)))
        _r = _power / 75
        if _power < 50:  # not even moving
            continue
        sleep(0.1)

        self.prev = self.now
        self.now = light.get_lightness()
        if _debug_color and abs(self.prev - self.now) > 5:
            print("COLOR value change: ", self.prev, ' ', self.now)
        # GETTING BRIGHTER
        if _r*B_TO_G > self.now - self.prev > _r*G_TO_W:
            if self.color == 'green':
                self.color = 'white'
                print("COLOR: change from GREEN 2 WHITE")
            elif self.color == 'black':
                self.color = 'green'
                print("COLOR: change from BLACK 2 GREEN")
        elif _r*B_TO_G < self.now - self.prev and self.color == 'black':
            self.color = 'white'
            print("COLOR: change from BLACK 2 WHITE")

        # GETTING DARKER
        if _r*B_TO_G > self.prev - self.now > G_TO_W*_r:
            if self.color == 'green':
                self.color = 'black'
                print("COLOR: change from GREEN 2 BLACK")
            elif self.color == 'white':
                self.color = 'green'
                print("COLOR: change from WHITE 2 GREEN")
        elif B_TO_G < self.prev - self.now and self.color == 'white':
            self.color = 'green'
            print("COLOR: change from WHITE 2 BLACK")


class Color:
    def __init__(self, sensor, calibrate_by='white'):
        self.sensor = sensor
        self.prev = sensor.get_lightness()
        self.now = sensor.get_lightness()
        self.color = calibrate_by
        work = Thread(target=_monitor, args=(self,))
        work.start()

    def __call__(self, *args, **kwargs):
        if args != ():
            return any([i == self.color for i in args])
        return self.color
