import time
import datetime # use to make nice print statement
import board
import busio
import adafruit_sht31d
import RPi.GPIO as GPIO

from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_sht31d.SHT31D(i2c)

def print_stats(duration, humidity, temperature, dhumidity, dtemp, dhdt, dTdt):
    """This function prints some super cool statistics"""
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
    # enable fan pin and heater pin as outputs
    for pin in fan_pin, heater_pin:
        GPIO.setup(pin, GPIO.OUT)

    # initialize last_loop variables
    last_time = time.time()
    last_humidity = sensor.relative_humidity
    last_temp = sensor.temperature

    # run forever
    while True:
        # get readings from sensor
        current_time = time.time()
        humidity = sensor.relative_humidity
        temperature = sensor.temperature
        # calculate how long we need to sleep for to roughly reach period
        duration = current_time - last_temp
        delay = duration - period
        if delay < 0:
            delay = 0
        time_to_sleep = period - delay

        # do cool calculations
        dhumidity = humidity - last_humidity
        dtemp = temperature - last_temp
        dhdt = dhumidity / duration
        dTdt = dtemp / duration

        # check if we need to turn heater on/off
        on_temp, off_temp = heater_range
        if temperature < on_temp:
            GPIO.output(heater_pin, GPIO.HIGH)
        elif temperature > off_temp:
            GPIO.output(heater_pin, GPIO.LOW)

        # check if we need to turn fan on/off
        on_humidity, off_humidity = fan_range
        if humidity < on_humidity:
            # is this right? we turn on the fan to INCREASE humidity????
            GPIO.output(fan_pin, GPIO.HIGH)
        elif humidity > off_humidity:
            GPIO.output(fan_pin, GPIO.LOW)

        # print super sexy text
        print_stats(duration=duration, humidity=humidity,
                    temperature=temperature, dhumidity=dhumidity,
                    dtemp=dtemp, dhdt=dhdt, dTdt=dTdt)

        # update last times for next loop
        last_humidity = humidity
        last_temp = temperature
        last_time = current_time

        # don't sleep if the last loop took more that 2x period seconds
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

# run the main() script if we are running this Python file
if __name__ == "__main__":
    main()
