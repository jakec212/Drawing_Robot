import numpy as np

radius = 2
num_points = 50  # Number of discrete points
theta = np.linspace(0, 2*np.pi, num_points)  # Angles from 0 to 2π

x_points = radius * np.cos(theta)  # X-coordinates
y_points = radius * np.sin(theta) + 9.75  # Y-coordinates


print("X:", x_points)
print("Y:", y_points)

x1 = -5.5
y1 = 8.5 + 5.5
# x1 = 0
# y1 = 0

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

    sa = da*800/360  #number of steps shoulder motor should take
    sb = db*800/360  #number of steps elbow motor should take

    return (sa, sb)


import numpy as np

x = np.concatenate(([x1], x_points, [x1]))
y = np.concatenate(([y1], y_points, [y1]))



print("yes")
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

#print(a)
#print(b)

print(ma)           #Shoulder motor stepper location (These values are where the stepper motor is at in relation to the starting point 0,0)
print(mb)  

#--------------------------------------------------------------------------------------------

import serial
import time

# Open serial connection (Update COM port for Windows or use "/dev/ttyUSB0" on Linux/Mac)
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # Wait for the connection to establish

def send_steps(ma, mb):
    # Send all step data to the Arduino without waiting for a response after each send
    for i in range(len(ma)):
        message = f"{ma[i]},{mb[i]}\n"  # Format: "motor1_steps,motor2_steps"
        arduino.write(message.encode())  # Send as bytes
        # Optionally, you can print what is being sent for debugging
        print(f"Sent: {message.strip()}")


send_steps(ma, mb)

# Close the serial connection after sending all data
arduino.close()