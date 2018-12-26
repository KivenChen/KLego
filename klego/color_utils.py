'''
now this module maintains a color object
by detecting how fast the brightness is changing
instead of using fixed thresholds
'''

from threading import Thread
from time import sleep


_debug_color_change = False


def _monitor_color(inst):
    print("COLOR: initializing, 1 second to wait")
    sleep(1)
    print("COLOR: ready")
    # well ... I'm pretty sure only ONE second is needed actually
    # because if core module is yet to be loaded, the importation will run into error
    from core import L, R
    to_be_verified = False

    while True:
        l_power, r_power = L._get_new_state().power, R._get_new_state().power
        _power = max((abs(l_power), abs(r_power)))
        _r = 1  # sensitivity

        if inst.color == 'green':
            pass
        if not inst.activate:
            continue
        if l_power * r_power <= 0:  # stopped or spinning
            # continue
            _r = 1.5
            pass
        if l_power < 0 and r_power < 0:  # backward
            # continue
            pass
        # if _power < 50:  # not even moving
        #   continue
        '''
        inst.history.pop()
        inst.history.insert(0, inst.now)
        inst.prev = sum(inst.history[4:]) / (len(inst.history) - 4)
        inst.reset()
        inst.now = sum(inst.history[:4]) / 4
        '''
        inst.prev = inst.now
        inst.now = inst.sensor.get_lightness()
        '''
        if inst._debug_refresh:
            print (inst.prev, inst.now)

        if inst._debug_color and abs(inst.prev - inst.now) > 12:
            print "COLOR value change: ", inst.prev, ' to ', inst.now, ', now', inst.color.upper()

        # GETTING BRIGHTER
        if inst.now - inst.prev > _r*inst.G_TO_W and inst.color == 'green':
                inst.color = 'white'
                inst.reset()
                print "COLOR: change from GREEN 2 WHITE" if _debug_color_change else ''
        elif _r*inst.B_TO_G < inst.now - inst.prev < _r*inst.B_TO_W and inst.color == 'black':
                inst.color = 'green'
                inst.reset()
                print "COLOR: change from BLACK 2 GREEN" if _debug_color_change else ''
        elif _r*inst.B_TO_W < inst.now - inst.prev and inst.color == 'black':
            inst.color = 'white'
            inst.reset()
            print "COLOR: change from BLACK 2 WHITE" if _debug_color_change else ''

        # GETTING DARKER
        if _r*inst.B_TO_W > inst.prev - inst.now > inst.G_TO_W*_r and inst.color == 'white':
            inst.color = 'green'
            inst.reset()
            print("COLOR: change from WHITE 2 GREEN")
        elif _r*inst.B_TO_G < inst.prev - inst.now < _r*inst.G_TO_W and inst.color == 'green':
            inst.color = 'black'
            inst.reset()
            print("COLOR: change from GREEN 2 BLACK")
        elif _r*inst.B_TO_W < inst.prev - inst.now:
            if inst.color == 'white':
                inst.color = 'black'
                inst.reset()
                print("COLOR: change from WHITE 2 BLACK")
        '''
        if inst.now > 340:
            inst.color = 'white'
        elif 200 < inst.now < 340:
            if 200 < inst.prev < 340:
                inst.color = 'green'
        else:
            inst.color = 'black'
        sleep(0.1)

class Color:
    def __init__(self, sensor, calibrate_by='white'):
        self.sensor = sensor
        self.history = [sensor.get_lightness() for i in range(10)]
        self.now = sensor.get_lightness()
        self.color = calibrate_by
        self.activate = True

        self._debug_global = False
        self._debug_color = True
        self._debug_refresh = True

        self.B_TO_G = 50 // 2.5
        self.G_TO_W = 80 // 2.5
        self.B_TO_W = self.B_TO_G + self.G_TO_W

        work = Thread(target=_monitor_color, args=(self,), name='color')
        work.start()

    def reset(self):
        def _work(self):
            self.history = [(self.sensor.get_lightness(), sleep(0.015))[0] for i in range(10)]
        _work(self)
        # Thread(target=_work, args=(self,)).start()

    def __call__(self, *args, **kwargs):
        if args != ():
            return any([i == self.color for i in args])
        return self.color
