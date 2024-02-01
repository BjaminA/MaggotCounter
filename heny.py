import time
import datetime  # Used for getting the current time for timestamping
import board
import busio
import adafruit_sht31d
import RPi.GPIO as GPIO

from time import sleep

# Set up GPIO pins using Broadcom SOC channel numbering
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Create library object for the SHT31-D sensor using I2C port
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_sht31d.SHT31D(i2c)

def print_stats(duration, humidity, temperature, dhumidity, dtemp, dhdt, dTdt):
    """Prints sensor statistics with timestamp."""
    timestamp = datetime.datetime.now().isoformat()
    print(
        f"{timestamp}: Duration={duration} s, Humidity={humidity} %, "
        f"Temperature={temperature} °C, ΔT={dtemp} °C, ΔRH={dhumidity} %, "
        f"ΔT/Δt={dTdt} °C/s, ΔRH/Δt={dhdt} %/s"
    )

def main(
    fan_pin=17, heater_pin=18, period=5,
    heater_range=[20, 25], fan_range=[70, 80],
):
    """Controls fan and heater based on sensor readings."""
    # Set the fan and heater pins as outputs
    for pin in fan_pin, heater_pin:
        GPIO.setup(pin, GPIO.OUT)

    # Initialise variables to store the last loop's data
    last_time = time.time()
    last_humidity = sensor.relative_humidity
    last_temp = sensor.temperature

    # Continuous loop for sensor reading and control
    while True:
        # Get current time and sensor readings
        current_time = time.time()
        humidity = sensor.relative_humidity
        temperature = sensor.temperature

        # Calculate time delay to maintain the desired loop period
        duration = current_time - last_time
        delay = duration - period
        time_to_sleep = max(0, period - delay)

        # Calculate changes in humidity and temperature
        dhumidity = humidity - last_humidity
        dtemp = temperature - last_temp
        dhdt = dhumidity / duration
        dTdt = dtemp / duration

        # Control heater based on temperature
        on_temp, off_temp = heater_range
        if temperature < on_temp:
            GPIO.output(heater_pin, GPIO.HIGH)  # Turn on heater
        elif temperature > off_temp:
            GPIO.output(heater_pin, GPIO.LOW)   # Turn off heater

        # Control fan based on humidity
        on_humidity, off_humidity = fan_range
        if humidity < on_humidity:
            GPIO.output(fan_pin, GPIO.HIGH)     # Turn on fan
        elif humidity > off_humidity:
            GPIO.output(fan_pin, GPIO.LOW)      # Turn off fan

        # Print the sensor statistics
        print_stats(duration=duration, humidity=humidity,
                    temperature=temperature, dhumidity=dhumidity,
                    dtemp=dtemp, dhdt=dhdt, dTdt=dTdt)

        # Update the last loop's data
        last_humidity = humidity
        last_temp = temperature
        last_time = current_time

        # Sleep to maintain the loop period
        if time_to_sleep > 0:
            sleep(time_to_sleep)

# Execute the main function when the script is run
if __name__ == "__main__":
    main()
