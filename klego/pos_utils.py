from math import sin, sqrt, cos, radians as rad
from core import _stop, going_back, going_forward, stopped, turning, _get_counts, robot_diameter
from time import sleep
from threading import Thread
from pos_calc import *
'''
this file provides the utilities for tracking robot and boxes locations
the **core** module will import this file and create *boxes* and *pos* for use
I will consider separating this util files from *nav_utils*
so that the core tech of coordinating will not be open-sourced
'''


class Position(object):
	def __init__(self, x=0, y=0, d=0):
		self.x = x
		self.y = y
		self.d = d
		self.accurate = True

	def track(self, d_delta, dpm, continuous=False):
		# tracks the position change
		# d_delta: the change of direction clockwise
		# dpm: the displacement x
		# continuous: handle f() and b() separately
		if continuous:
			pass
		self.d += d_delta
		dx = dpm * sin(rad(self.d))
		dy = dpm * cos(rad(self.d))
		self.x += dx
		self.y += dy
		return self

	def dist(self, pos):
		# output distance
		return sqrt((self.x-pos.x)**2+(self.y - pos.y)**2)

	def __str__(self):
		return '%d, %d, direction: %d' % (self.x, self.y, self.d)

	def __call__(self, *args, **kwargs):
		return self.x, self.y, self.d


class PositionTracker(Position):
	def __init__(self):
		super(PositionTracker, self).__init__()
		self.interval = 0.1
		orig_l, orig_r = _get_counts()
		self.prevL = orig_l  # previous tacho count
		self.prevR = orig_r

	def reset(self):
		"""reset the tacho count base and the numbers
		"""
		orig_l, orig_r = _get_counts()
		self.prevL = orig_l
		self.prevR = orig_r
		self.x = 0
		self.y = 0
		self.d = 0

	@staticmethod
	def _turnlen_to_dgr(turn_len):

		pass

	def _monitor(self):
		while True:
			sleep(self.interval)
			nowL, nowR = _get_counts()
			deltaL = nowL - self.prevL
			deltaR = nowR - self.prevR
			dx, dy, dD = poscalc(deltaL, deltaR, robot_diameter)

			self.x += dx*sin(rad(self.d))
			self.y += dy*cos(rad(self.d))
			self.d += degrees(dD)

			self.prevL = nowL
			self.prevR = nowR

	def activate(self):
		Thread(target=self._monitor).start()


class Box(Position):
	def __init__(self, x=0, y=0, d=0, ok=True):
		super(Box, self).__init__()
		self.x = x
		self.y = y
		self.d = d
		self.new = ok  # marks if this is ok-to-go


class Boxes(list):
	def __init__(self):
		super(Boxes, self).__init__()

	def add(self, inst, new=True):
		if isinstance(inst, Position):
			inst = Box(inst.x, inst.y, inst.d, new)
		self.append(inst)
		return self
	
	def nearest(self, robo_pos):
		# return the nearest and ok-to-go box
		target = 0
		min_dist = 99999
		for i, box in enumerate(self):
			dist = robo_pos.dist(box.pos)
			if dist < min_dist and box.new:
				min_dist = dist
				target = box
		return target

	def overlapped(self, target_pos, threshold=14):
		# check if the target is already discovered
		if type(target_pos) == Box:
			target_pos = target_pos.pos
		for i, box in enumerate(self):
			if box.dist(target_pos) <= threshold:
				return True
		return False


def test():
	b1 = Box(10, 20)
	b2 = Box(10, 20)
	print(b2.x)
	boxes = Boxes()
	boxes.add(b1)
	boxes.add(b2)
	print(boxes[1])
	print(boxes)


if __name__ == "__main__":
	test()
