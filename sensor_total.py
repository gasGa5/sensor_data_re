import time
import board
import adafruit_dht
import RPi.GPIO as GPIO
import requests
import numpy as np
import datetime

import bmp

from network.push_dat import send_data

# DHT 센서 및 GPIO 핀 설정
dhtDevice = adafruit_dht.DHT11(board.D17)
gas_pin = 23
led_pin = 25
pulse_pin = 20
vibration_pin = 18

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(gas_pin, GPIO.IN)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(pulse_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(vibration_pin, GPIO.IN)

# 변수 초기화
is_running = True
totalflow = 0
p_1liter = 5880 / 2

# current data send time 
last_data_sent_time = datetime.datetime.now()

try:
    while is_running:
        try:
            # DHT11 센서에서 온도 및 습도 읽기
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * 9 / 5 + 32
            humidity = dhtDevice.humidity
            print("Temperature: {:.1f} F / {:.1f} C\tHumidity: {}%".format(temperature_f, temperature_c, humidity))
        except RuntimeError as error:
            print("Failed to read DHT11 sensor data:", error)
        
        # 가스 센서 읽기
        gas_value = GPIO.input(gas_pin)
        if gas_value == 1:
            GPIO.output(led_pin, GPIO.HIGH)
            print("Gas Sensor - Detected")
        else:
            GPIO.output(led_pin, GPIO.LOW)
            print("Gas Sensor - Not Detected")
        
        # 펄스 센서 읽기
        status = GPIO.input(pulse_pin)
        t0 = time.time()
        count = 0
        
        while time.time() - t0 < 1:
            input_state = GPIO.input(pulse_pin)
            if input_state != status:
                count += 1
                status = input_state
        
        pulse_counted = count / 2
        flow_rate = pulse_counted / p_1liter * 1000
        totalflow += pulse_counted
        print("Number of pulses:", pulse_counted)
        print("Flow rate:", flow_rate, "ml/sec")
        print("Total flow:", totalflow, "ml")
        
        # 진동 센서 읽기
        start_time = time.time()
        vibration_count = 0
        
        while time.time() - start_time < 1:
            input_state = GPIO.input(vibration_pin)
            if input_state == GPIO.HIGH:
                vibration_count += 1
            time.sleep(0.1)
        
        print("Vibration count:", vibration_count)

        # air presure
        bus = bmp.smbus.SMBus(1)
    
        bmp.init_Calibration_Data()
        # temp = bmp.read_Temperature()
        pressure = bmp.read_Pressure()
        # altitude = bmp.read_Altitude()

        current_time = datetime.datetime.now()
        unix_timestamp = int(time.mktime(current_time.timetuple())) * 1000  
        data = {
            "time": [unix_timestamp],
            "temperature": temperature_c if 'temperature_c' in locals() else np.random.normal(20, 2), # get input
            "humidity": humidity if 'humidity' in locals() else np.random.normal(50, 5), # get input
            "flux1": np.random.normal(10, 1),
            "flux2": np.random.normal(10, 1),
            "flux3": np.random.normal(10, 1),
            "flux4": np.random.normal(10, 1),
            "flex": pressure if 'pressure' in locals() else 1, # idk default of preasure
            "air_quality": gas_value if 'gas_value' in locals() else np.random.randint(0, 501), # get input
            "tilt1": np.random.normal(0, 5),
            "tilt2": np.random.normal(0, 5),
            "tilt3": np.random.normal(0, 5),
            "tilt4": np.random.normal(0, 5),
            "vibe1": vibration_count if 'vibration_count' in locals() else np.random.normal(0, 2), # get input
            "vibe2": np.random.normal(0, 2)
        }

        current_time_s = datetime.datetime.now()

        # 3 second interval
        if (current_time - last_data_sent_time).total_seconds() >= 3:
            response = send_data(data)
            print("code: ", response)

            last_data_sent_time = current_time

except KeyboardInterrupt:
    print("Program interrupted by user.")
except Exception as e:
    print("Error : ")
    print(e)
finally:
    GPIO.cleanup()
