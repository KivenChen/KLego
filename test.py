from core import *

move = SynchronizedMotors(L, R, 0.5)
move.turn(100, 360)
stop()
move.turn(100, 360)