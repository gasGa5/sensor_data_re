import time
import board
import adafruit_dht
import RPi.GPIO as GPIO
import requests
import numpy as np
import datetime
import asyncio

# custom library
import bmp
import flux

from network.push_dat import send_data

# DHT and GPIO pin
dhtDevice = adafruit_dht.DHT11(board.D17)
gas_pin = 23
led_pin = 25
# pulse_pin = 20
vibration_pin = 18

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(gas_pin, GPIO.IN)
GPIO.setup(led_pin, GPIO.OUT)
# GPIO.setup(pulse_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
flux.setup()
GPIO.setup(vibration_pin, GPIO.IN)

# state and constant
is_running = True
totalflow = 0
# flow filter
p_1liter = 5880 / 2
# for flux
count = 0

# current data send time 
last_data_sent_time = datetime.datetime.now()

async def main():
    try:
        while is_running:
            try:
                # DHT11 read
                temperature_c = dhtDevice.temperature
                temperature_f = temperature_c * 9 / 5 + 32
                humidity = dhtDevice.humidity
            except RuntimeError as error:
                print("Failed to read DHT11 sensor data:", error)

            # gas digital input
            gas_value = GPIO.input(gas_pin)
            if gas_value == 1:
                GPIO.output(led_pin, GPIO.HIGH)
                print("Gas Sensor - Detected")
            else:
                GPIO.output(led_pin, GPIO.LOW)
                print("Gas Sensor - Not Detected")

            #########################################
            # pulse for flow input
            current_flux_call = time.time()
            flow_rate = await flux.loop()
            # flow_rate = flux.loop(current_flux_call)
            # flow calculate
            # pulse_counted = count / 2
            totalflow = flux.total_flow
            ##########################################
            ##########################################

            # vibe / sec
            start_time = time.time()
            vibration_count = 0

            while time.time() - start_time < 1:
                input_state = GPIO.input(vibration_pin)
                if input_state == GPIO.HIGH:
                    vibration_count += 1
                time.sleep(0.1)

            # air presure
            bus = bmp.smbus.SMBus(1)

            bmp.init_Calibration_Data()
            pressure = bmp.read_Pressure()

            # data format
            # (include virtual data)
            current_time = datetime.datetime.now()
            unix_timestamp = int(time.mktime(current_time.timetuple())) * 1000  
            data = {
                "time": [unix_timestamp],
                "temperature": temperature_c if 'temperature_c' in locals() else np.random.normal(20, 2), # get input
                "humidity": humidity if 'humidity' in locals() else np.random.normal(50, 5), # get input
                "flux1": flow_rate if 'flow_rate' in locals() else np.random.normal(10, 1),
                "flux2": np.random.normal(10, 1),
                "flux3": np.random.normal(10, 1),
                "flux4": np.random.normal(10, 1),
                "flex": abs(pressure) if 'pressure' in locals() else 1, # idk default of preasure
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
                print("preasure: ", abs(pressure))
                print("Temperature: {:.1f} F / {:.1f} C\tHumidity: {}%".format(temperature_f, temperature_c, humidity))
                print("Vibration count:", vibration_count)

                # print("Number of pulses:", pulse_counted)
                print("Flow rate:", flow_rate, "ml/sec")
                print("Total flow:", totalflow, "ml")

                last_data_sent_time = current_time

    except KeyboardInterrupt:
        print("Program interrupted by user.")
    except Exception as e:
        print("Error : ")
        print(e)
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    asyncio.run(main())