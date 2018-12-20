import core
from core import brightness, stop
from time import sleep
from core import *
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
		self._debug = False

		# tunable numeric value
		# get it a zero to disable a function

		''' PID fundamental parameters '''
		"""NOTE: kp tuning
		Moreover, 0.3, 0.4 are also helpful under some circumstances
		Night time: 0.15 ( where brightness around 250 - 350), ki and kp should also be kept smaller
		Night time (under a light) kp 0.17, ki and kp should not change
		Day time: 0.2 (where brightness around 550 to 650), ki 0.02 - 0.04, kd 0.05
		Except Cross Night config: 0.15 0.01 0.03
		
		"""

		'tp 85 -> kp est 0.5'
		'tp 90 -> kp est 0.6 <- interval 0.01'
		'tp 95 -> kp est ef'
		self.kp = 0.4  # learning rate
		self.ki = self.kp / 30  # integral weight
		self.kd = self.kp / 40  # derivative

		'''environmental parameters.  '''
		"""NOTE: the offset should be tuned"""
		self.offset = 275  # tune with calibrate_offset(), the brightness for half black, half white
		self.tp = 85  # power value when the robot is cruising on a straight line
		self.interval = 0.01  # a float t. Update the brightness info every t seconds
		self.finish_line_brightness = 380
		self.cross_threshold = 0

		''' data postprocessing '''
		self.history_len = 20
		self.reversive_boundary = 70  # as boundary of
		self.clip_oscl = 999  # disallow any greater gap between L, R motor power
		self.min_oscl = 0  # force oscillation
		self.alignment = 0.
		self.critical_light_reverse = 0

		''' contextual callback '''
		self._callback_conditions = ["brightness() > finish_line"]
		self._callback_execs = [("return True",)]
		
	def encountered_cross(self):
		"""
		judge if the robot has encountered a cross
		:return: bool
		"""
		return self.cross_threshold > brightness()

	def when(self, condition, *callbacks):
		"""
		register callbacks to PID controller
		:param condition: string oode to run
		:param callbacks: to execute
		:return:
		"""
		assert \
			type(condition) == str and \
			all([type(i) == str for i in callbacks]),\
			"the condition and the callbacks must be executable expression/code in str"
		self._callback_conditions.append(condition)
		self._callback_execs.append(callbacks)
	
	def _handle_callback(self):
		"""
		this function handles registered callbacks
		:return:
		"""
		for i, c in enumerate(self._callback_conditions):
			if eval(c):
				for exe_code in self._callback_execs[i]:
					exec exe_code

	def effective(self, value):
		'''
		:param value: original value
		:return: adjusted power value
		'''
		_complement = 1.1
		
		''' prepare for power reverse '''
		reversive_boundary = self.reversive_boundary
		delta = reversive_boundary - value
		
		''' power reverse and clipping '''
		if reversive_boundary > value:
			value = (-reversive_boundary-delta) * _complement
		value = np.clip(value, -127, 127)  # the motor.run() function can only accepts a value between -127 and 127
		return value

	def save_model(self, fpath):
		np.save(fpath, np.asarray([self]))

	def _verified_light(self, light):
		bound = self.critical_light_reverse
		if light < bound:
			delta = bound - light
			alarm()
			return bound + delta
		return light

	@staticmethod
	def load(fpath):
		cont = np.load(fpath)
		return cont[0]

	def __str__(self):
		return 'kp: %.3f, ki: %.3f, kd: %.3f, offset: %d, tp: %d'\
			% (self.kp, self.ki, self.kd, self.offset, self.tp)

	def __call__(self, *args, **kwargs):
		return str(self)

	def calibrate_offset(self):
		from core import spin
		bottom1 = brightness()
		_, light1 = spin(0.3), brightness()
		_, light2 = spin(-0.6), brightness()
		spin(0.3)
		bottom2 = brightness()
		avg_light = (light1 + light2) // 2
		print(avg_light)
		avg_bottom = (bottom1 + bottom2) // 2
		print(avg_bottom)
		self.offset = (avg_bottom + avg_light) // 2
		return self.offset

	def run(self):
		if self.offset == -1:
			raise ValueError("Please invoke pid.calibrate_offset() first")
		if self.kp == -1:
			raise ValueError("kp and only kp is not preset. Please assign value manually")
		# tunable parameters
		kp = self.kp
		ki = self.ki
		kd = self.kd
		finish_line = self.finish_line_brightness
		interval = self.interval
		offset = self.offset  # todo: mean of brightness
		tp = self.tp

		# non-tunnable parameters

		integral_history = []
		lasterror = 0
		L = core.L
		R = core.R
		_r = 1

		guard_window(stop)
		counter = 0
		# main loop
		while not core._stop :
			''' update environment '''
			light = self._verified_light(brightness())
			error = light - offset

			''' handling callback '''
			self._handle_callback()

			
			'''applying PID foundamental algorithm'''
			
			integral_history.insert(0, error)
			integral = sum(integral_history)
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
				continue
			
			'''NOTE: clip oscillation is an experimental feature'''
			if abs(turn) > self.clip_oscl:
				continue
				# turn = self.clip_oscl

			powerL = tp + turn  * _r
			powerR = tp - turn  * _r
			# print(type(self.effective(powerR)))
			if self._debug:
				print (powerL, ' ', powerR)

			'''apply clipping through effective()'''
			L.run(self.effective(powerL))
			R.run(self.effective(powerR))
			lasterror = error
			sleep(interval)
		return False
