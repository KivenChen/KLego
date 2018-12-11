from math import sin, cos, tan, sqrt, radians as r

'''
this file provides the utilities for tracking robot and boxes locations
the **core** module will import this file and create *boxes* and *pos* for use
I will consider separating this util files from *nav_utils*
so that the core tech of coordinating will not be open-sourced
'''

class Position:
	x = 0
	def __init__(self):
		self.x = 0.0
		self.y = 0.0
		self.d = 0
		self.accurate = True
	
	def track(self, d_delta, dpm, continuous=False):
		# tracks the position change
		# d_delta: the change of direction clockwise
		# dpm: the displacement x
		# continuous: handle f() and b() separately
		if continuous：
			pass
		self.d += d_delta
		dx += dpm * sin(r(d))
		dy += dpm * cos(r(d))
		
	def from(self, pos):
		# output distance
		return math.sqrt((self.x-pos.x)**2+(self.y - pos.y)**2)

class Box:
	def __init__(self, pos, ok=True):
		self.pos = pos
		self.go = ok


class Boxes(list):
	def __init__(self):
		pass
	
	def add(self, pos, go):
		self.append(Box(pos, go))
		
	
	def nearest(self, robo_pos):
		min = 0
		mindist = 99999
		for i, box in enumerate(self):
			dist = robo_pos.from(box.pos)
			if dist < mindist and box.go: 
				mindist = dist
				min = box
		return min
		
