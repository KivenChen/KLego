from core import *

def run():
	kp = 10
	ki = 1
	kd = 100
	offset = 45 # todo: mean of brightness
	tp = 50
	integral = 0
	lasterror = 0
	deriv = 0
	while True:
		light = brightness()
		error = light - offset
		integral += error
		deriv = error-lasterror
		turn = kp*error + ki*integral+kd*deriv
		powerL = tp+turn
		powerR = tp-turn
		L.run(powerL)
		R.run(powerR)
		lasterror = error
