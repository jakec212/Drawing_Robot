import numpy as np
from robot import Robot
from shape import Circle, Rectangle
from pathplanner import acceleration_plan, velocity_plan 

# Pick what it is you woud like to draw and generate xy coordinates
# Define how you are planning to communicate. Discrete points? or continuous motion?
    # This is where you would define the time for continuous motion
# Generate the path of points or generate the continuous motion velocity path/list
points = 1000
time =3
dt = time/points
t = np.linspace(0, time, points)
x_circle_center = 0
y_circle_center = 5.5 + 8.5/2

robot = Robot()
circle = Circle(x_circle_center, y_circle_center, radius=2.0, num_points= points)
start_x = robot.starting_position[0]
start_y = robot.starting_position[1]
p_x, p_y = circle.path(start_x, start_y)
s_ma, s_mb = robot.steps(p_x, p_y)
va, vb = velocity_plan(s_ma, s_mb, t)
a_a, a_b = acceleration_plan(va, vb, t)
# At this point the velocity and steps are only local

#---------------------------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt

# The path has the start/end point added on each end, so rebuild t
# to have the same number of points as the step arrays
t = np.linspace(0, time, len(s_ma))

plt.figure()
plt.plot(t, s_ma, marker='o', label="Base (Shoulder) Motor")
plt.plot(t, s_mb, marker='o', label="Elbow Motor")
plt.xlabel("Time (s)")
plt.ylabel("Step Position (steps)")
plt.title("Motor Step Positions vs Time")
plt.legend()
plt.grid(True)

plt.figure()
plt.step(t, va, where='post', label="Base (Shoulder) Motor")
plt.step(t, vb, where='post', label="Elbow Motor")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (steps per second)")
plt.title("Motor Velocities vs Time")
plt.legend()
plt.grid(True)

plt.figure()
plt.plot(t, a_a, label="Base (Shoulder) Motor")
plt.plot(t, a_b, label="Elbow Motor")
plt.xlabel("Time (s)")
plt.ylabel("Acceleration (steps per second$^2$)")
plt.title("Motor Accelerations vs Time")
plt.legend()
plt.grid(True)

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
