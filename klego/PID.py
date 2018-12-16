import core
from core import brightness
from time import sleep
from core import stop
from guard import *
import numpy as np
import atexit
atexit.register(stop)


class PID_Controller:
	def __init__(self, debug=False):
		# dev ops
		self._debug = False

		# tunable numeric value
		# get it a zero to disable a function

		''' PID fundamental parameters '''
		self.kp = 0.2  # learning rate
		self.ki = 0.01  # integral
		self.kd = 0.02  # derivative

		'''environmental parameters.  '''
		self.offset = -1  # tune with calibrate_offset(), the brightness for half black, half white
		self.tp = 75  # power value when the robot is cruising on a straight line
		self.interval = 0.02  # a float t. Update the brightness info every t seconds

		''' data postprocessing '''
		self.clip = 65  # as boundary of
		self.critical_gap = 40  # disallow any greater gap between L, R motor power
		self.force_oscl = 20  # force oscillation


	def effective(self, value):
		# clip the effective value by 60
		# because power lower than that will not work
		clip = self.clip
		delta = clip - abs(value)
		if clip > value > 0:
			return -clip-delta
		else:
			return value


	def save_model(self, fpath):
		np.save(fpath, np.asarray([self]))

	@staticmethod
	def load(fpath):
		cont = np.load(fpath)
		return cont[0]

	def __str__(self):
		return 'kp: %d, ki: %d, kd: %d, offset: %d, tp: %d'\
			% (self.kp, self.ki, self.kd, self.offset, self.tp)

	def calibrate_offset(self):
		from core import spin
		bottom1 = brightness()
		_, light1 = spin(0.1), brightness()
		_, light2 = spin(-0.2), brightness()
		spin(0.1)
		bottom2 = brightness()
		avg_light = (light1 + light2) // 2
		print(avg_light)
		avg_bottom = (bottom1 + bottom2) // 2
		print(avg_bottom)
		self.offset = (avg_bottom + avg_light) // 2
		return self.offset

	def run(self):
		# tunable parameters
		kp = self.kp
		ki = self.ki
		kd = self.kd
		interval = self.interval
		offset = self.offset  # todo: mean of brightness
		tp = self.tp

		# non-tunnable parameters

		integral = 0
		lasterror = 0
		L = core.L
		R = core.R

		guard_window(stop)

		# main loop
		while not core._stop:
			light = brightness()
			error = light - offset
			integral += error
			deriv = error - lasterror
			turn = kp * error + ki * integral + kd * deriv

			if self.force_oscl > turn > 0:
				turn = self.force_oscl
			elif -self.force_oscl < turn < 0:
				turn = -self.force_oscl

			'''NOTE: critical_gap is an experimental feature'''
			if abs(turn) > self.critical_gap:
				turn = self.critical_gap if turn > 0 else - self.critical_gap

			powerL = tp - turn
			powerR = tp + turn
			print powerL, ' ', powerR if self._debug else 0
			L.run(self.effective(powerL))
			R.run(self.effective(powerR))
			lasterror = error
			sleep(interval)