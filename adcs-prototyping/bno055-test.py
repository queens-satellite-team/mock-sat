import board
import busio
import time
import adafruit_bno055

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

for x in range(50):
	print('ANGLE: {}' .format(sensor.euler))
	eul = sensor.euler
	print(eul[0])
	time.sleep(0.5)

