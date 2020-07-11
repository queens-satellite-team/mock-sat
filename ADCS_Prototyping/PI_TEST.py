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
time.sleep(0.1)

#set control pins on pi - note that 18 is the only hardware PWM pin on 3B+ model
PWM_CTRL = 18
PWM_FREQ = 100
DIR_CTRL = 15

#set tolerances on angles and velocities
TOL_EUL = 1 #degrees
TOL_VEL = 0.1 #rad/sec

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
time.sleep(0.1)

DES_EUL = int(input('Enter desired orientation (between 0 and 360):'))
print('Desired angle is: {}' .format(DES_EUL))

def eul(): #returns orientation in degrees
	try:
		EUL = int(sensor.euler[0])
		if EUL > 360:
			EUL = EUL%360
	except:
		print('ERROR IN EULER ANGLE READ')
		EUL = eul()
	return EUL

def vel(): #returns angular velocity in rads/sec
	try:
		VEL = int(sensor.gyro[0])
	except:
		print('ERROR IN VELOCITY READ')
		VEL = vel()
	return VEL

#def detumble(): #could be changed simply to apply magnetorquers instead of wheels
#        VEL = vel()
#        if VEL > 0:
#                IO.output(DIR_CTRL, IO.HIGH)
#        else:
#                IO.output(DIR_CTRL, IO.LOW)
#
#        M.ChangeDutyCycle(

for x in range(500):
	VEL = vel()
#        if VEL > TOL_VEL:
#               detumble()

	EUL = eul()
	DIFF = DES_EUL - EUL
	if abs(DIFF) < TOL_EUL:
		time.sleep(0.01)
		continue

	if abs(DIFF) > 270:
		DIFF = (-1)*abs(abs(DIFF) - 360)*DIFF/abs(DIFF)

#	print('P control DIFF')
#	print(DIFF/2)

	DIFF = DIFF/3 + (VEL*180/3.14)/6

#	print('PI control DIFF')
#	print(DIFF)

	#define direction
	if DIFF > 0:
		IO.output(DIR_CTRL, IO.LOW)
	elif DIFF < 0:
		IO.output(DIR_CTRL, IO.HIGH)

	DUTY = 100 - abs(DIFF) #converty to duty percentage

#	if abs(DUTY - DUTY_PREV) > 10: #max acc
#		DUTY = DUTY_PREV + 10*(DUTY_PREV - DUTY)/abs(DUTY_PREV - DUTY)

#	if abs(DUTY - DUTY_PREV) < 2 and DUTY != 100 and DUTY != DUTY_PREV: #min acc
#		DUTY = DUTY_PREV + 2*(DUTY_PREV - DUTY)/abs(DUTY_PREV - DUTY)

	if DUTY < 10: #max vel
		DUTY = 10
	elif DUTY > 100: #no vel
		DUTY = 100

	DUTY_PREV = DUTY

	print(EUL)
	print(DIFF)
	print(DUTY)

	M.ChangeDutyCycle(int(DUTY))
	time.sleep(0.01)

M.stop()
IO.cleanup()
