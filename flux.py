import RPi.GPIO as GPIO
import time

flowPin = 20
flowRate = 0.0
total_flow = 0.0
count = 0

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(flowPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(flowPin, GPIO.RISING, callback=flow_callback, bouncetime=20)
    print("Setup complete")

def loop():
    global count,total_flow
    count = 0
    time.sleep(1)
    flowRate = count * 0.27
    # flowRate *= 60
    # flowRate /= 1000
    # print(count)
    total_flow = total_flow + flowRate 
    print(f'flowrate:{flowRate} mL/sec')
    print(f'total_flow:{total_flow} mL')
def flow_callback(channel):
    global count
    count += 1

if __name__ == '__main__':
    setup()
    try:
        while True:
            loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
