'''
now this module maintains a color object
by detecting how fast the brightness is changing
instead of using fixed thresholds
'''

from threading import Thread
from time import sleep

def _handle_green_separately(self):
    if self.color == 'green':
        pass


def _monitor(self):
    print("COLOR: initializing, 1 second to wait")
    sleep(1)
    # well ... I'm pretty sure only ONE second is needed actually
    # because if core module is yet to be loaded, the importation will run into error
    from core import L, R

    while True:
        l_power, r_power = L._get_new_state().power, R._get_new_state().power
        _power = max((abs(l_power), abs(r_power)))
        _r = 1  # sensitivity

        if self.color == 'green':
            pass
        if not self.activate:
            continue
        if l_power * r_power <= 0:  # stopped or spinning
            # continue
            _r = 2
            pass
        if l_power < 0 and r_power < 0:  # backward
            # continue
            pass
        if _power < 50:  # not even moving
            continue
        sleep(0.05)

        _handle_green_separately(self)

        self.history.pop()
        self.history.insert(0, self.now)
        self.prev = sum(self.history[4:]) / (len(self.history)-4)
        self.reset()
        self.now = sum(self.history[4:]) / (len(self.history)-4)

        if self._debug_color and abs(self.prev - self.now) > 12:
            print "COLOR value change: ", self.prev, ' to ', self.now, ', now', self.color.upper()

        # GETTING BRIGHTER
        if self.now - self.prev > _r*self.G_TO_W and self.color == 'green':
                self.color = 'white'
                self.reset()
                print "COLOR: change from GREEN 2 WHITE"
        elif _r*self.B_TO_G < self.now- self.prev < _r*self.B_TO_W and self.color == 'black':
                self.color = 'green'
                self.reset()
                print "COLOR: change from BLACK 2 GREEN"
        elif _r*self.B_TO_W < self.now - self.prev and self.color == 'black':
            self.color = 'white'
            self.reset()
            print "COLOR: change from BLACK 2 WHITE"

        # GETTING DARKER
        if _r*self.B_TO_W > self.prev - self.now > self.G_TO_W*_r and self.color == 'white':
            self.color = 'green'
            self.reset()
            print("COLOR: change from WHITE 2 GREEN")
        elif _r*self.B_TO_G < self.prev - self.now < _r*self.G_TO_W and self.color == 'green':
            self.color = 'black'
            self.reset()
            print("COLOR: change from GREEN 2 BLACK")
        elif _r*self.B_TO_W < self.prev - self.now:
            if self.color == 'white':
                self.color = 'black'
                self.reset()
                print("COLOR: change from WHITE 2 BLACK")


class Color:
    def __init__(self, sensor, calibrate_by='white'):
        self.sensor = sensor
        self.history = [sensor.get_lightness() for i in range(10)]
        self.now = sensor.get_lightness()
        self.color = calibrate_by
        self.activate = True

        self._debug_global = False
        self._debug_color = True

        self.B_TO_G = 70
        self.G_TO_W = 90
        self.B_TO_W = self.B_TO_G + self.G_TO_W

        work = Thread(target=_monitor, args=(self,))
        work.start()

    def reset(self):
        def _work(self):
            self.history = [(self.sensor.get_lightness(),
                             sleep(0.01)
                             )[0] for i in range(10)]
        _work(self)
        # Thread(target=_work, args=(self,)).start()

    def __call__(self, *args, **kwargs):
        if args != ():
            return any([i == self.color for i in args])
        return self.color
