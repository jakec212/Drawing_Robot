import numpy as np

shoulder_angle = 132.50559
elbow_angle = 137.88429

x1 = -5.5
y1 = 8.5 + 5.5

arm = 8.059

def motion(x, y):
    l = (x**2+y**2)**0.5

    a1 = np.arccos(x/l)
    a2 = np.arccos(l/2/arm)
    a3 = (np.pi/2-a2)*2              #angle of the elbow joint in degrees
    a4 = a2 + a1
                    #angle of the shoulder measured from 0 degrees 
    #print(a3, a4)
    a3 = a3*180/np.pi   #elbow angle in degrees
    a4 = a4*180/np.pi   #Shoulder Angle in degrees

    da = shoulder_angle - a4            #angle change that shoulder joint needs to make
    db = elbow_angle - a3        #angle change that elbow joint needs to make

    da = (8*da) *-1   #angle change that the shoulder stepper motor should take  (multiplied by -1 to account for the motor being flipped)
    db = 4*db      #angle change that the elbow stepper motor should take 

    sa = da*800/360  #number of steps shoulder motor should take
    sb = db*800/360  #number of steps elbow motor should take

    return (sa, sb)   #the step position of each motor that coorespond to a given x and y coordinate from the origin of the stepper motors

#----------------------------------------------------------------------------------

radius = 2
num_points = 500  # Number of discrete points
theta = np.linspace(0, 2*np.pi, num_points)  # Angles from 0 to 2π

x_points = radius * np.cos(theta)  # X-coordinates
y_points = radius * np.sin(theta) + 9.75  # Y-coordinates

sa, sb = motion(x_points, y_points)

sa = np.append(sa, 0)
sb = np.append(sb, 0)

sa = [round(num) for num in sa]
sb = [round(num) for num in sb]

#print(sa)
#print(sb)

#----------------------------------------------------------------------

import serial
import time

# Open serial connection (Update COM port for Windows or use "/dev/ttyUSB0" on Linux/Mac)
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # Wait for the connection to establish



def send_steps(ma, mb):
    for i in range(len(ma)):

        message = f"{ma[i]},{mb[i]}\n"  # Format: "motor1_steps,motor2_steps"
        arduino.write(message.encode())  # Send as bytes

        #arduino.write(f"{ma[i]}\n".encode())  # Send steps as a string - converts message into string.encode and writes it to the arduino

        while True:
            response = arduino.readline().decode().strip()
            if response == "Done":
                #print("Stepper motor movement completed. Onto the next one")
                break


# Example: Move the stepper motor to position 1000
send_steps(sa, sb)

arduino.close()
