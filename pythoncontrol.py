import numpy as np

radius = 2
num_points = 50  # Number of discrete points
max_time = 3  # Total time for the motion
theta = np.linspace(0, 2*np.pi, num_points)  # Angles from 0 to 2π
time = np.linspace(0, max_time, num_points)

x_points = radius * np.cos(theta)  # X-coordinates
y_points = radius * np.sin(theta) + 9.75  # Y-coordinates


print("X:", x_points)
print("Y:", y_points)

x1 = -5.5
y1 = 8.5 + 5.5
# x1 = 0
# y1 = 0

arm = 8.059

def angle(x, y):  #function passes in an xy coordinate and returns a base and elbow angle
    
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

    #the 8 and the 4 represent the geometry of the gears on the robot arm
    da = (8*da)    #angle change that the shoulder stepper motor should take
    db = 4*db *-1     #angle change that the elbow stepper motor should take (multiplied by -1 to account for the motor being flipped)


    sa = da*200*4/360  #number of steps shoulder motor should take
    sb = db*200*4/360  #number of steps elbow motor should take

    return (sa, sb)


import numpy as np

x = np.concatenate(([x1], x_points, [x1]))
y = np.concatenate(([y1], y_points, [y1]))



print("yes")
a = []
b = []

for i in range(len(x)):  #steps through the list of coordinates and appends an array for the angles that each point is
    c, d = angle(x[i], y[i])
    a.append(c)
    b.append(d)

ma = [0]
mb = [0]


for i in range(len(a)-1):  #steps through the array of angles and returns an array for the amount of steps needed for each spot
    e, f = motion(a[i], b[i], a[i+1], b[i+1])
    ma.append(ma[i] + e)
    mb.append(mb[i] + f)

ma = [round(num) for num in ma]
mb = [round(num) for num in mb]

#print(a)
#print(b)

print("printing ma and mb")
print(ma)           #Shoulder motor stepper location (These values are where the stepper motor is at in relation to the starting point 0,0)
print(mb)

#---------------------------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt

# x and y include the extra start/end point added above, so time needs to
# be recomputed to have the same number of points as x and y
t = np.linspace(0, max_time, len(x))

# Drawing of the path (x vs y)
plt.figure()
plt.plot(x, y, marker='o')
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Drawing Path")
plt.axis("equal")

# X and Y position over time
plt.figure()
plt.plot(t, x, marker='o', label="X")
plt.plot(t, y, marker='o', label="Y")
plt.xlabel("Time (s)")
plt.ylabel("Position")
plt.title("Position vs Time")
plt.legend()

# Motor 1 (shoulder) and Motor 2 (elbow) angles over time
plt.figure()
plt.plot(t, a, marker='o')
plt.xlabel("Time (s)")
plt.ylabel("Angle (degrees)")
plt.title("Motor 1 (Shoulder) Angle vs Time")

plt.figure()
plt.plot(t, b, marker='o')
plt.xlabel("Time (s)")
plt.ylabel("Angle (degrees)")
plt.title("Motor 2 (Elbow) Angle vs Time")

plt.show()

#---------------------------------------------------------------------------------------------------------------------


# import serial
# import time

# # Open serial connection (Update COM port for Windows or use "/dev/ttyUSB0" on Linux/Mac)
# arduino = serial.Serial('COM3', 9600, timeout=1)
# time.sleep(2)  # Wait for the connection to establish



# def send_steps(ma, mb):
#     for i in range(len(ma)):

#         message = f"{ma[i]},{mb[i]}\n"  # Format: "motor1_steps,motor2_steps"
#         arduino.write(message.encode())  # Send as bytes

#         #arduino.write(f"{ma[i]}\n".encode())  # Send steps as a string - converts message into string.encode and writes it to the arduino

#         while True:
#             response = arduino.readline().decode().strip()
#             if response == "Done":
#                 #print("Stepper motor movement completed. Onto the next one")
#                 break


# # Example: Move the stepper motor to position 1000
# send_steps(ma, mb)

# arduino.close()
