from core import *
import core
import atexit
atexit.register(stop)



def run():
	kp = 1000
	ki = 100
	kd = 10000
	offset = (core._GREEN_BLACK_BOUNDARY_ +core._GREEN_WHITE_BOUNDARY_)/2 - 5 # todo: mean of brightness
	tp = 50
	integral = 0
	lasterror = 0

	while True:
		light = brightness()
		error = light - offset
		integral += error
		deriv = error - lasterror
		turn = kp*error + ki*integral + kd*deriv
		turn /= 100
		powerL = tp + turn
		powerR = tp - turn
		print(powerL, ' ',powerR)
		L.run(powerL)
		R.run(powerR)
		lasterror = error

run()