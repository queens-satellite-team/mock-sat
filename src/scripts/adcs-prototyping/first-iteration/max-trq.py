try:
	import time
	import RPi.GPIO as IO
	IO.setmode(IO.BCM)
	IO.setwarnings(False)
	import board
	import busio
	#set i2c connection - note that pins 2 (SDA) and 3 (SCL) are the only i2c connections on pi 3B+ model
	i2c = busio.I2C(board.SCL, board.SDA)
	import adafruit_bno055 as bno
	sensor = bno.BNO055_I2C(i2c)
	TOL = 2 #angular tolerance
except:
	print('Error initializing BNO055 sensor')

print('BNO055 sensor reading initialized')
time.sleep(1)

#set control pins on pi - note that 18 is the only hardware PWM pin on 3B+ model
PWM_CTRL = 18
PWM_FREQ = 100
DIR_CTRL = 15

try:
	IO.setup(PWM_CTRL, IO.OUT)
	IO.setup(DIR_CTRL, IO.OUT)

	IO.output(DIR_CTRL, IO.HIGH)
	M = IO.PWM(PWM_CTRL, PWM_FREQ)
	DUTY = 100
	DUTY_PREV = DUTY
	M.start(DUTY)
except:
	print('Error initializing FIT0441 control signal')

print('FIT0441 control initialized')
time.sleep(1)
CHANGE = 1

for x in range(1, 100):
	M.ChangeDutyCycle(101 - x)
	time.sleep(0.05)

print('max vel')
time.sleep(1)
IO.output(DIR_CTRL, IO.LOW)
time.sleep(1)

M.stop()
IO.cleanup()
