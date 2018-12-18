import core
from core import brightness
from time import sleep
from core import stop
from guard import *
import numpy as np
import atexit
atexit.register(stop)
from random import uniform


def alarm():
	print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

class PID_Controller:
	def __init__(self, debug=False):
		# dev ops
		self._debug = True

		# tunable numeric value
		# get it a zero to disable a function

		''' PID fundamental parameters '''
		self.kp = 0.2  # learning rate
		self.ki = 0.02  # integral weight
		self.kd = 0.05  # derivative

		'''environmental parameters.  '''
		self.offset = 265  # tune with calibrate_offset(), the brightness for half black, half white
		self.tp = 80  # power value when the robot is cruising on a straight line
		self.interval = 0.01  # a float t. Update the brightness info every t seconds
		self.all_white_threshold = -1
		self.corss_threshold = -1

		''' data postprocessing '''
		self.history_len = 20
		self.reversive_boundary = 70  # as boundary of
		self.clip_oscl = 999  # disallow any greater gap between L, R motor power
		self.min_oscl = 0  # force oscillation
		self.alignment = 0.00


		''' contextual callback '''
		self._callback_conditions = []
		self._callback_funcs = []
	
	def all_white(self):
		return self.all_white_threshold < brightness()
		
	def encountered_cross(self):
		return self.cross_threshold < brightness()
		
				
	def when(self, condition, callback):
		# register a callback when certain condition is satisfied
		# assert(type(condition) != str, "condition and callback must be executable expression/code in str")
		# assert(type(callback) != str, "condition and callback must be executable expression/code in str")
		
		self._callback_conditions += [condition]
		self._callback_funcs += [callback]
		# not yet ready for function-oriented programming
		# self._callback_args += [(*args, **kwargs)]
	
	def _handle_callback(self):
		for i, c in enumerate(self._callback_conditions):
			if eval(c):
				eval(self._callback_funcs[i])
				
			
	def effective(self, value):
		# clip the effective value by 60
		# because power lower than that will not work
		'''_complement is an experimental feature'''
		_complement = 1.1
		
		''' prepare for power reverse '''
		reversive_boundary = self.reversive_boundary
		delta = reversive_boundary - value
		
		''' power reverse and clipping '''
		if reversive_boundary > value:
			output = (-reversive_boundary-delta) * _complement
			if output > 127:  # the motor.run() accepts only a value betw -127 ~ 127
				return 127
			elif output < -127:
				return -127
			else:
				return output
		else:
			if value > 127:
				return 127
			elif value < -127:
				return 127
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

	def __call__(self, *args, **kwargs):
		return str(self)

	def calibrate_offset(self):
		from core import spin
		bottom1 = brightness()
		_, light1 = spin(0.2), brightness()
		_, light2 = spin(-0.4), brightness()
		spin(0.2)
		bottom2 = brightness()
		avg_light = (light1 + light2) // 2
		print(avg_light)
		avg_bottom = (bottom1 + bottom2) // 2
		print(avg_bottom)
		self.offset = (avg_bottom + avg_light) // 2
		return self.offset

	def run(self):
		if self.offset == -1:
			raise ValueError("Please invoke calibrate_offset() first")
		# tunable parameters
		kp = self.kp
		ki = self.ki
		kd = self.kd
		interval = self.interval
		offset = self.offset  # todo: mean of brightness
		tp = self.tp

		# non-tunnable parameters

		integral_history = 0
		lasterror = 0
		L = core.L
		R = core.R
		_r = 1

		guard_window(stop)

		# main loop
		while not core._stop:
			''' handling callback '''
			self._handle_callback()
			
			'''applying PID foundamental algorithm'''
			light = brightness()
			error = light - offset
			
			integral_history += [error]
			integral_history.pop() if len(integral_history) > self.history_len else 0
			
			deriv = error - lasterror
			turn = kp * error + ki * integral + kd * deriv
			
			'''applying force oscillation'''
			if self.min_oscl > turn > 0:
				turn = self.min_oscl
			elif -self.min_oscl < turn < 0:
				turn = -self.min_oscl

			'''applying alignment'''
			if uniform(0, 1) < self.alignment:
				_r = - _r
			
			'''NOTE: clip oscillation is an experimental feature'''
			if abs(turn) > self.clip_oscl:
				continue
				# turn = self.clip_oscl

			powerL = tp + turn  * _r
			powerR = tp - turn  * _r
			# print(type(self.effective(powerR)))
			print (powerL, ' ', powerR) if self._debug else ''

			'''apply clipping through effective()'''
			L.run(self.effective(powerL))
			R.run(self.effective(powerR))
			lasterror = error
			sleep(interval)
