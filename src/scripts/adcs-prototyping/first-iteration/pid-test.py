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
	M.start(100)
except:
	print('Error initializing FIT0441 control signal')

print('FIT0441 control initialized')
time.sleep(1)

DES_EUL = int(input('Enter desired orientation (between 0 and 360):'))
print('Desired angle is: {}' .format(DES_EUL))

for x in range(0, 1000):
	try:
		EULER = sensor.euler
		EUL = EULER[0]
		if EULER[0] > 360:
			EUL = EUL%360

		elif ~isinstance(EUL, int):
			EUL = 1/0

	except:
		print('Error in sensor reading')



	try:
		DIFF = DES_EUL - EUL
		if abs(DIFF) > 220:
			DIFF = -1*(360 - abs(DIFF))*DIFF/abs(DIFF)

		print('Current Difference: {}' .format(DIFF))
		if DIFF < -10 and DIFF > -300:
			IO.output(DIR_CTRL, IO.HIGH)
			DUTY = int(99 - abs(DIFF))
			print('Applied duty: {}' .format(DUTY))
			M.ChangeDutyCycle(DUTY)
		elif DIFF >= -10 and DIFF <= 10:
			M.ChangeDutyCycle(100)
		elif DIFF > 10 and DIFF < 300:
			IO.output(DIR_CTRL, IO.LOW)
			DUTY = int(99 - abs(DIFF))
			print('Applied duty: {}' .format(DUTY))
			M.ChangeDutyCycle(DUTY)
	except:
		print('Error in signal application')

	time.sleep(0.05)

M.stop()
IO.cleanup()
