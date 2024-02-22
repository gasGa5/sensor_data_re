import RPi.GPIO as GPIO
import time
import asyncio

flowPin = 23
flowRate = 0.0
total_flow = 0.0
count = 0
current_time = time.time()

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(flowPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(flowPin, GPIO.RISING, callback=flow_callback, bouncetime=20)
    print("Setup complete")

# loop is return flowRate
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

    return flowRate
    
# async def loop():
#     global count, total_flow

#     while True:
#         count = 0  # 펄스 카운트 초기화
#         await asyncio.sleep(1)  # 비동기 sleep

#         flowRate = count * 0.27
#         total_flow += flowRate
#         return flowRate

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
