from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import skeletonize
from skimage.util import invert

# --- Step 1: Create the image of the letter "A" ---
width, height = 100, 100
letter = "A"

# Create a white canvas
img = Image.new("L", (width, height), color=255)
draw = ImageDraw.Draw(img)

# Choose a font and size
font = ImageFont.truetype("arial.ttf", 80)

# Get size of text to center it
bbox = draw.textbbox((0, 0), letter, font=font)
text_x = (width - (bbox[2] - bbox[0])) // 2
text_y = (height - (bbox[3] - bbox[1])) // 2

# Draw the letter
draw.text((text_x, text_y), letter, fill=0, font=font)

# --- Step 2: Convert to binary and skeletonize ---
img_array = np.array(img)
binary = img_array < 128  # Convert to binary: black = True
skeleton = skeletonize(binary)

# --- Step 3: Extract coordinates ---
y_coords, x_coords = np.nonzero(skeleton)  # Nonzero gives (rows = y, cols = x)

# --- Step 4: Visualize the path ---
plt.figure(figsize=(6, 6))
plt.imshow(skeleton, cmap="gray")
plt.plot(x_coords, y_coords, 'r.', markersize=1)
plt.gca().invert_yaxis()  # So origin is bottom-left like robot coords
plt.title("Skeleton Path of Letter A")
plt.axis("off")
plt.show()

y_coords = [y + 9.75 for y in y_coords]  # Add 9.75 to each element

#-------------------------------------------------------------

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
# Convert lists to NumPy arrays
x_coords = np.array(x_coords)
y_coords = np.array(y_coords)

print(x_coords)
print(y_coords)

sa, sb = motion(x_coords, y_coords)

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
