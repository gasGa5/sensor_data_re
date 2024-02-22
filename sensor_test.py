import time
import board
import adafruit_dht
import RPi.GPIO as GPIO
import requests
import numpy as np
import datetime
from bmp_test import bmp180
from network.push_dat import send_data

# DHT 센서 및 GPIO 핀 설정
# dhtDevice = adafruit_dht.DHT11(board.D17)
# gas_pin = 23
# led_pin = 25
# pulse_pin = 20
# vibration_pin = 18

class sensor_read():
    def __init__(self,):
        self.dhtDevice = adafruit_dht.DHT11(board.D27)
        self.bmp = bmp180(0x77) 
        self.interval_time = 1
        self.gas_pin1 = 17
        self.gas_pin2 = 24
        self.led_pin = 25
        self.pulse_pin = 23
        self.vibration_pin = 22
        self.flowRate = 0.0
        self.total_flow = 0.0
        self.flow_count = 0
        self.mL_per_pulse = 0.27
        self.vibration_count = 0
        self.gas_value = None
        self.temperature_c = None
        self.humidity = None
        self.is_running = True
        self.pressure = None
        
    def setup(self,) -> None:
        # GPIO 설정
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gas_pin1, GPIO.IN)
        GPIO.setup(self.gas_pin2, GPIO.IN)
        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.setup(self.pulse_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.vibration_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.gas_pin1, GPIO.FALLING, callback=self.gas1_interrupt_callback, bouncetime=200)
        GPIO.add_event_detect(self.gas_pin2, GPIO.FALLING, callback=self.gas2_interrupt_callback, bouncetime=200)
        # GPIO.add_event_detect(self.led_pin, GPIO.RISING, callback=flow_callback, bouncetime=20)
        GPIO.add_event_detect(self.pulse_pin, GPIO.RISING, callback=self.flow_callback, bouncetime=20)
        GPIO.add_event_detect(self.vibration_pin, GPIO.RISING, callback=self.vibration_interrupt_callback, bouncetime=300)
         
    def sensor_loop(self,) -> None:
        self.flow_count = 0
        self.vibration_count = 0
        self.gas_value = 0
        time.sleep(self.interval_time)
        self.flowRate = self.flow_count * self.mL_per_pulse
        self.total_flow = self.total_flow + self.flowRate
        self.pressure = self.bmp.get_pressure()/101325
        self.DHT11_read()
        if self.gas_value == 1:
            print(f'Gas Sensor - Detected')
            GPIO.output(self.led_pin, GPIO.HIGH)
        else:
            print("Gas Sensor - Not Detected")
            GPIO.output(self.led_pin, GPIO.LOW)
        print(f'temperature_c:{self.temperature_c} , humidity:{self.humidity}')
        print(f'pressure:{self.pressure}')
        print(f'vibration:{self.vibration_count}')
        print(f'flowrate:{self.flowRate} mL/sec')
        print(f'total_flow:{self.total_flow} mL\n')

        return {
            "temparature" : self.temperature_c,
            "humidity" : self.humidity,
            "presure" : self.pressure,
            "vibration" : self.vibration_count, # hz
            "flowRate":self.flowRate,
            "gas_value": self.gas_value # 0,1
        }
            
    def flow_callback(self,channel):
        self.flow_count += 1

    def DHT11_read(self,):
        try:
            # DHT11 센서에서 온도 및 습도 읽기
            self.temperature_c = self.dhtDevice.temperature
            self.humidity = self.dhtDevice.humidity
        
        except RuntimeError as error:
            print("Failed to read DHT11 sensor data:", error)
             

    def gas1_interrupt_callback(self,channel):
        # 가스 센서 읽기
        self.gas_value = 1
        
    def gas2_interrupt_callback(self,channel):
        self.gas_value = 1
        print('gas2')
      
    def vibration_interrupt_callback(self,channel):
        self.vibration_count += 1

    def run(self,):
        last_data_sent_time = datetime.datetime.now()
        try:
            while self.is_running:
                try:
                    sensor_data = self.sensor_loop()

                    current_time = datetime.datetime.now()
                    unix_timestamp = int(time.mktime(current_time.timetuple())) * 1000  


                    data = {
                        "time": [unix_timestamp],
                        "temperature": sensor_data["temparature"], # get input
                        "humidity":  sensor_data["humidity"], # get input
                        "flux1": sensor_data["flowRate"],
                        "flux2": np.random.normal(10, 1),
                        "flux3": np.random.normal(10, 1),
                        "flux4": np.random.normal(10, 1),
                        "flex": abs(sensor_data["presure"]), # idk default of preasure
                        "air_quality": sensor_data["gas_value"], # get input
                        "tilt1": np.random.normal(0, 5),
                        "tilt2": np.random.normal(0, 5),
                        "tilt3": np.random.normal(0, 5),
                        "tilt4": np.random.normal(0, 5),
                        "vibe1": sensor_data["vibration"], # get input
                        "vibe2": np.random.normal(0, 2)
                    }

                    # 3 second interval
                    if (current_time - last_data_sent_time).total_seconds() >= 3:
                        response = send_data(data)
                        print("response : ", response)
                        last_data_sent_time = current_time
                except RuntimeError as error:
                    print("Failed to read sensor data:", error)

        except KeyboardInterrupt:
            print("Program interrupted by user.")
        except Exception as e:
            print("Error : ")
            print(e)
        finally:
            GPIO.cleanup()
            
if __name__ == '__main__':
    sensor = sensor_read()
    sensor.setup()
    sensor.run()
