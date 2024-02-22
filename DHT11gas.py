import time
import board
import adafruit_dht
import RPi.GPIO as GPIO

dhtDevice=adafruit_dht.DHT11(board.D27)

gas_pin=17
# led_pin=25
GPIO.setmode(GPIO.BCM)
is_running=True
GPIO.setup(gas_pin, GPIO.IN)
# GPIO.setup(led_pin ,GPIO.OUT)

try:
	while True:
		try:
			temperature_c=dhtDevice.temperature
			temperature_f=temperature_c*((9/5)+32)
			humidity=dhtDevice.humidity
			print("Temp: {:.1f} F / {:.1f} C	Humidity: {}%".format(temperature_f, temperature_c, humidity))
		except RuntimeError as error:
			print("Failed to read DHT11 sensor data:", error)
		
		gas_value=GPIO.input(gas_pin)
		if gas_value==1:
			# GPIO.output(led_pin,GPIO.HIGH)
			print("Gas Sensor - Detected")
		else:
			# GPIO.output(led_pin,GPIO.LOW)
			print("Gas Sensor - Not Detected")

		time.sleep(2.0)

except KeyboardInterrupt:
	GPIO.cleanup()
