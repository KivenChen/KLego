from core import *
import random

global direction #方向

f(None)
if black(): #碰到黑色反弹
    stop()
    brick(1)
    spin(r=-180)
if distance()<=10: #碰到障碍物
    if green(): #判断是得分块
        f(p=75,t=None) #减慢速度 接近
        if distance()<=5: #相当于press
            stop()
            sound()
            brick(1) #能不能后退一段距离呢？就是以cm为单位的距离
            direction=random.randint(90,270)
            spin(r=direction)
        else:
            brick(1)
            direction=random.randint(90,270)
            spin(r=direction)