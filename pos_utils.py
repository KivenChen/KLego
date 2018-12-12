from math import sin, sqrt, cos, radians as rad

'''
this file provides the utilities for tracking robot and boxes locations
the **core** module will import this file and create *boxes* and *pos* for use
I will consider separating this util files from *nav_utils*
so that the core tech of coordinating will not be open-sourced
'''

# forward and left when see dark
# forward and right when see light


class Position:
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


class Box(Position):
	def __init__(self, x=0, y=0, d=0, ok=True):
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
		min = 0
		mindist = 99999
		for i, box in enumerate(self):
			dist = robo_pos.dist(box.pos)
			if dist < mindist and box.new:
				mindist = dist
				min = box
		return min

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
	print(boxes._discover(Position(30, 15, 45), 5))
	print(boxes)


if __name__ == "__main__":
	test()
