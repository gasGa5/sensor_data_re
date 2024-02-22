import RPi.GPIO as GPIO

# SW-420 센서가 연결된 GPIO 핀 번호
sensor_pin = 22

# 진동 감지 횟수 초기화
vibration_count = 0

def vibration_callback(channel):
    global vibration_count
    vibration_count += 1
    print("진동이 감지되었습니다. 현재 진동 횟수:", vibration_count)

# GPIO 핀 모드 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_pin, GPIO.IN)

# 진동 감지 이벤트 핸들러 등록
GPIO.add_event_detect(sensor_pin, GPIO.RISING, callback=vibration_callback, bouncetime = 100)

try:
    while True:
        pass

except KeyboardInterrupt:
    print("프로그램이 종료되었습니다.")

finally:
    # GPIO 설정 초기화
    GPIO.cleanup()
