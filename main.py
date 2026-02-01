import subprocess
import time
import os

# Path to your Arduino CLI and sketch
arduino_cli_path = "arduino-cli"  # Assumes arduino-cli is in PATH, if it isn't then run: sudo snap install arduino-cli
sketch_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sketch_jan15a")
arduino_sketch = os.path.join(sketch_dir, "sketch_jan15a.cpp")
arduino_port = "/dev/cu.usbmodem1101"  # Adjust for your system (e.g., COM3 on Windows)
arduino_board = "esp8266:esp8266:nodemcuv2"  # ESP8266 board for VL53L5CX with Wire.begin(6, 7) 

# Compile and upload Arduino sketch
compile_cmd = [
    arduino_cli_path, "compile", "--fqbn", arduino_board, arduino_sketch
]
upload_cmd = [
    arduino_cli_path, "upload", "-p", arduino_port, "--fqbn", arduino_board, arduino_sketch
]

subprocess.run(compile_cmd, check=True)
subprocess.run(upload_cmd, check=True)

time.sleep(2)

subprocess.run(["python3", "tof_matrix_viz.py"], check=True)