from klego import *

def run():
    pid.kp = 0.4
    pid.offset = 236
    pid.offset = 308
    pid.when("encountered_cross()", "")
    pid.when("brightness() > 342", "None")
    pid.run()