# tof_sensor_setup

1. Clone the VL53L5CX library:
   ```bash
   git clone https://github.com/sparkfun/SparkFun_VL53L5CX_Arduino_Library.git
   ```

2. Install Arduino CLI:
   ```bash
   sudo snap install arduino-cli
   ```

3. Install ESP32 board support:
   ```bash
   # For ESP32:
   arduino-cli core update-index
   arduino-cli core install esp32:esp32
   ```

4. Find your board and port:
   ```bash
   arduino-cli board list
   ```