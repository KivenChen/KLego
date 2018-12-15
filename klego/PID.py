from core import *
import core
import atexit
atexit.register(stop)


class PID_Controller:
	def __init__(self, debug=False):
		self.kp = 1000
		self.ki = 100
		self.kd = 10000
		self._debug = False
		self.offset = (core.GREEN_BLACK_BOUNDARY + core.GREEN_WHITE_BOUNDARY) / 2

	def run(self):
		# tunable parameters
		kp = self.kp
		ki = self.ki
		kd = self.kd
		interval = 0.05
		offset = self.offset  # todo: mean of brightness

		# non-tunnable parameters
		tp = 50
		integral = 0
		lasterror = 0
		# main loop
		while not core._stop:
			light = brightness()
			error = light - offset
			integral += error
			deriv = error - lasterror
			turn = kp * error + ki * integral + kd * deriv
			turn /= 100
			powerL = tp + turn
			powerR = tp - turn
			print powerL, ' ', powerR if self._debug else 0
			L.run(powerL)
			R.run(powerR)
			lasterror = error
			sleep(interval)
