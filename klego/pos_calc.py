from math import sin, cos, degrees


def to_cm(tcounts):
	return tcounts / 20


def poscalc(dCl, dCr, dmt):
	""" this function calcs the delta displacements and the delta direction
	param:
	dCl, dCr: the change of tacho counts of both motors
	dmt: the diameter. Or the distance between two wheels
	returns:
	dx, dy, dDirection in radians
	NOTE that dx, dy corresponds to the previous direction
	"""
	if dCl == dCr:
		C = (dCl + dCr) // 2
		return 0, to_cm(C), 0
		
	CM = max(dCl, dCr)
	Cm = min(dCl, dCr)
	lambd = CM / (CM - Cm)
		
	D = (lambd - 0.5) * dmt
	theta = 2*to_cm(CM) / D  # todo: implement to_cm function
	
	dy = D * sin(theta)
	dx = D * (1 - cos(theta))
	
	return dx, dy, theta

