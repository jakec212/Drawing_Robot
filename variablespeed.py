import numpy as np

x1 = -5.5
y1 = 8.5 + 5.5

x2 = -x1
y2 = y1

arm = 8.059

def angle(x, y):
    
    l = (x**2+y**2)**0.5
    print(x)
    print(l)
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


x = [x1, x2]
y = [y1, y2]

a1 = []
a2 = []

for i in range(len(x)):
    a, b = angle(x[i], y[i])
    a1.append(a)
    a2.append(b)

sa = [0]
sb = [0]

for i in range(len(a1)-1):
    e, f = motion(a1[i], a2[i], a1[i+1], a2[i+1])
    sa.append(sa[i] + e)
    sb.append(sb[i] + f)

print(sa)
print(sb)

print(angle(x1, y1))
