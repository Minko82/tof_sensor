import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import re

# ---------------- CONFIGURATION ---------------- #
# CHANGE THIS to match your Arduino's port
SERIAL_PORT = '/dev/cu.usbmodem101'
BAUD_RATE = 115200
# Set the max distance (in mm) for the color scale
MAX_DISTANCE_MM = 2000 
# ----------------------------------------------- #

# Initialize Serial Connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {SERIAL_PORT}")
except Exception as e:
    print(f"Error connecting to serial port: {e}")
    exit()

# Setup the Plot
fig, ax = plt.subplots()
# Create an empty 8x8 matrix
data_matrix = np.zeros((8, 8))
# Create the heatmap image
# 'viridis' is a good color map, 'plasma' is also good for heat
im = ax.imshow(data_matrix, cmap='viridis', vmin=0, vmax=MAX_DISTANCE_MM)
plt.colorbar(im, label='Distance (mm)')
ax.set_title("VL53L5CX 8x8 Matrix")

# Add text annotations for each cell (optional, can be slow if computer is old)
text_annotations = [[ax.text(j, i, '', ha="center", va="center", color="w", fontsize=6) 
                     for j in range(8)] for i in range(8)]

def update(frame):
    global data_matrix
    raw_lines = []
    
    # We need to read enough lines to form a frame. 
    # Your Arduino code outputs 8 rows + 1 empty line per frame.
    # We read until the buffer is clear or we have enough data.
    
    while ser.in_waiting:
        try:
            line = ser.readline().decode('utf-8').strip()
            # Only process lines that contain data (look for digits)
            print(f"Raw data: {line}")
            if len(line) > 0 and line[0].isdigit():
                # Split by tab or space
                parts = re.split(r'\s+', line)
                # Filter out empty strings and convert to int
                nums = [int(p) for p in parts if p.isdigit()]
                
                # If we parsed a row correctly (should be 8 numbers)
                if len(nums) == 8:
                    raw_lines.append(nums)
            
            # If we have collected 8 rows, we have a full frame
            if len(raw_lines) == 8:
                # Update the matrix
                data_matrix = np.array(raw_lines)
                
                # Update the image data
                im.set_data(data_matrix)
                
                # Update the text numbers inside the squares
                for i in range(8):
                    for j in range(8):
                        val = data_matrix[i, j]
                        text_annotations[i][j].set_text(str(val))
                        # Change text color based on brightness for readability
                        text_annotations[i][j].set_color('black' if val > MAX_DISTANCE_MM/2 else 'white')
                
                # Clear buffer for the next frame
                raw_lines = []
                # Flush input to avoid lag
                ser.reset_input_buffer()
                return [im] + [t for row in text_annotations for t in row]

        except ValueError:
            pass # Ignore malformed lines
        except Exception as e:
            print(f"Error: {e}")

    return [im]

# Run the animation
ani = FuncAnimation(fig, update, interval=50, blit=False) # 50ms refresh rate
plt.show()

ser.close()
