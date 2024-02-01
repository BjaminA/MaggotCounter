README: Raspberry Pi Sensor Control Program
Overview
This program is designed to run on a Raspberry Pi for controlling environmental conditions using sensors. Specifically, it interfaces with a temperature and humidity sensor (SHT31-D) and controls a fan and a heater based on the sensor readings. It is ideal for applications such as greenhouse environments, laboratory experiments, or any situation where maintaining specific temperature and humidity levels is crucial.

Features
Real-time Sensor Monitoring: Utilises the SHT31-D sensor for accurate temperature and humidity measurements.
Automatic Control: Manages a fan and a heater to regulate environmental conditions.
Adaptive Loop Timing: Maintains consistent measurement intervals.
Data Logging: Records sensor readings with timestamps for analysis and tracking.
Requirements
Hardware: Raspberry Pi (any model with GPIO pins), SHT31-D temperature and humidity sensor, compatible fan and heater with GPIO controllable relays.
Software: Python 3.x, Adafruit SHT31-D Python library, RPi.GPIO library.
Installation and Setup
Hardware Setup: Connect the SHT31-D sensor to the Raspberry Pi via the I2C interface. Connect the fan and heater to designated GPIO pins (default are GPIO 17 for the fan and GPIO 18 for the heater) through relay modules.
Software Setup: Install the necessary Python libraries (adafruit-circuitpython-sht31d and RPi.GPIO) using pip.
Script Configuration: Modify the script to match your specific hardware setup, particularly the GPIO pin numbers and sensor I2C address if different from the defaults.
Usage
Running the Program: Execute the script using Python 3. The program enters an infinite loop, continuously reading sensor data and controlling the fan and heater.
Monitoring and Logging: The program prints sensor readings and control actions to the console with timestamps. This data can be redirected to a file for logging purposes.
Customisation
Adjustable Parameters: You can adjust parameters such as the temperature and humidity thresholds for turning the fan and heater on and off within the script.
Sensor and Pin Configuration: Change the GPIO pin assignments and sensor parameters if different from the defaults.
Safety and Precautions
Ensure all hardware connections are secure and correctly wired.
Be cautious when working with electrical appliances like heaters and fans.
Always test the system in a safe environment before deploying it in critical applications.
Support
For any queries or issues with setting up or running the program, please refer to the Raspberry Pi and sensor documentation or community forums for support.
