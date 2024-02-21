import RPi.GPIO as GPIO
import time

flow_sensor_pin = 20  # YF-S401 센서의 펄스 출력 핀에 연결된 GPIO 핀 번호

GPIO.setmode(GPIO.BCM)
GPIO.setup(flow_sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

flow_rate = 0.0
total_liters = 0.0
last_read_time = time.time()

def pulse_callback(channel):
    global flow_rate, total_liters, last_read_time
    if GPIO.input(channel):
        flow_rate += 1.0
    else:
        liters_per_pulse = 4.5  # YF-S401 센서의 1 펄스 당 유량 (예시 값)
        flow_rate -= 1.0 / liters_per_pulse

        if flow_rate < 0.0:
            flow_rate = 0.0

        total_liters += (1.0 / liters_per_pulse)
        last_read_time = time.time()

GPIO.add_event_detect(flow_sensor_pin, GPIO.BOTH, callback=pulse_callback)

while True:
    try:
        time.sleep(1)
        current_time = time.time()
        time_elapsed = current_time - last_read_time
        if time_elapsed >= 5.0:  # 5초 동안 펄스가 없으면 유량을 0으로 간주
            flow_rate = 0.0
        print("유량: {:.2f} L/min, 누적 유량: {:.2f} L".format(flow_rate, total_liters))
    except KeyboardInterrupt:
        break

GPIO.cleanup()
