import RPi.GPIO as GPIO
import time

SENSOR_PIN=24	# data pin number
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

vibration_count=0

start_time=time.time()

try:
	while True:
		print("Start")
		start_time = time.time()
		vibration_count = 0
		#input_state=GPIO.input(SENSOR_PIN)

		while time.time() - start_time < 1:
			input_state = GPIO.input(SENSOR_PIN)
			print(input_state)
			if input_state == GPIO.HIGH:
				vibration_count += 1
			time.sleep(0.1)
		print("COUNT:", vibration_count)
finally:
	GPIO.cleanup()

