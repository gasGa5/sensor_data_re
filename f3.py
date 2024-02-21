import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
pulse_pin = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(pulse_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 변수 초기화
status = GPIO.input(pulse_pin)
t0 = time.time()
count = 0
totalflow = 0
p_1liter = 5880 / 2 

try:
    while True:
        # Read current pulse status
        input_state = GPIO.input(pulse_pin)

        # Increase count each time the pulse state changes
        if input_state != status:
            count += 1
            status = input_state
    
        # Calculate and output every second
        if time.time() - t0 >= 1:
            pulse_counted = count / 2
            flow_rate = (pulse_counted / p_1liter) *1000
            totalflow += pulse_counted
            print("number of pulse", pulse_counted)
            print("flowrate:", flow_rate, "ml/sec")
            print("total flow:", totalflow, "ml")
            count = 0
            t0 = time.time()

except KeyboardInterrupt:
    print("Program finish")
finally:
    GPIO.cleanup()
