import numpy as np
import math

x1 = -5.5
y1 = 8.5 + 5.5

arm = 8.059

def angle(x, y):
    
    l = (x**2+y**2)**0.5
    
    a1 = np.arccos(x/l)
    a2 = np.arccos(l/2/arm)
    a3 = (np.pi/2-a2)*2              #angle of the elbow joint in degrees
    a4 = a2 + a1
                    #angle of the shoulder measured from 0 degrees 
    #print(a3, a4)
    a3 = a3*180/np.pi
    a4 = a4*180/np.pi
    return (a4, a3)   #angle of each joint in degrees


def motion(a1, b1, a2, b2):
    da = a2 - a1            #angle change that each joint needs to make
    db = b2 - b1

    da = (8*da)    #angle change that the shoulder stepper motor should take
    db = 4*db *-1     #angle change that the elbow stepper motor should take (multiplied by -1 to account for the motor being flipped)

    sa = da*200/360  #number of steps shoulder motor should take
    sb = db*200/360  #number of steps elbow motor should take

    return (sa, sb)


x = [x1, -1.5, -1.5, 1.5, 1.5,-1.5, x1]
y = [y1, 11.25, 8.25, 8.25, 11.25, 11.25, y1]

a = []
b = []

for i in range(len(x)):
    c, d = angle(x[i], y[i])
    a.append(c)
    b.append(d)

ma = [0]
mb = [0]


for i in range(len(a)-1):
    e, f = motion(a[i], b[i], a[i+1], b[i+1])
    ma.append(ma[i] + e)
    mb.append(mb[i] + f)

ma = [round(num) for num in ma]
mb = [round(num) for num in mb]

print(a)
print(b)
print(ma)           #Shoulder motor stepper location (These values are where the stepper motor is at in relation to the starting point 0,0)
print(mb)           #Elbow motor stepper location

a, b = angle(x1, y1)

a1 = [26.11, a]
a2 = [46.61, b]

m1, m2 = motion(26.11, 46.11, a, b)

print(m1)
print(m2)