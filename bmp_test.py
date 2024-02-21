import smbus2
import time

# I2C 버스 번호와 BMP180 센서의 주소 설정
bus = smbus2.SMBus(1)
address = 0x77

# BMP180 센서 초기화
bus.write_byte_data(address, 0xf4, 0x2e)
time.sleep(0.005)

# 온도 값 읽어오기
temp_raw = bus.read_i2c_block_data(address, 0xf6, 2)
temp = ((temp_raw[0] << 8) + temp_raw[1]) / 10.0

# 압력 값 읽어오기
pressure_raw = bus.read_i2c_block_data(address, 0xf6, 3)
pressure = ((pressure_raw[0] << 16) + (pressure_raw[1] << 8) + pressure_raw[2]) / 100.0

print("Temperature: {} °C".format(temp))
print("Pressure: {} hPa".format(pressure))
