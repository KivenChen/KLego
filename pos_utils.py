'''
this file provides the utilities for tracking robot and boxes locations
the **core** module will import this file and create *boxes* and *pos* for use
I will consider separating this util files from *nav_utils*
so that the core tech of coordinating will not be open-sourced
'''

class Position:
	x = 0
	def __init__(self):
		self.x = 0
		self.y = 0
		self.d = 0
		self.accurate = True
	
	def track(self, d_delta, dpm, continuous=False):
		# tracks the position change
		# d_delta: the change of direction clockwise
		# dpm: the displacement x
		# continuous: handle f() and b() separately
		pass


class Boxes(list):
	def __init__(self):
		pass
	
	def add(self, pos, is_bonus):
		Boxes.append([pos.x, pos.y, pos.d])
		
	
	
