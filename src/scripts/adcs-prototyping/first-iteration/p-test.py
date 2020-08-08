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
time.sleep(1)

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

def desaturate(DUTY): #relies on friction of system for wheel desaturation - actual satellite uses magnetorquers
	print('Desaturating')
	for x in range(DUTY, 100):
		M.ChangeDutyCycle(x)
		time.sleep(0.1)

def detumble(): #removes satellite momentum via repeatedly spinning up wheels and desaturating
	print('Detumbling')
	VEL = vel()
	momentRatio = 2
	DUTY = momentRatio*abs(VEL)
	DUTY_PREV = 100
	while VEL > TOL_VEL:
		VEL = vel()
		DUTY = momentRatio*abs(VEL)
		if VEL < 0:
			IO.output(DIR_CTRL, IO.HIGH)
		elif VEL > 0:
			IO.output(DIR_CTRL, IO.LOW)
		if DUTY > 100:
			DUTY = 100
		elif DUTY < 5:
			DUTY = 5
		if DUTY_PREV == DUTY:
			desaturate(DUTY)
		M.ChangeDutyCycle(DUTY)
		DUTY_PREV = DUTY
		time.sleep(0.1)

	if DUTY < 100:
		desaturate(DUTY)

def kick(DUTY):
	print('Kicking')
	desaturate(DUTY)
	EUL_STUCK = eul()
	EUL = eul()
	while EUL_STUCK == EUL:
		DUTY = 50
		M.ChangeDutyCycle(DUTY)
		time.sleep(0.5)
		desaturate(DUTY)
		EUL = eul()

def rotate(): #rotates satellite to desired euler angle
	print('Rotating')
	VEL = vel()
	if VEL > TOL_VEL:
		detumble()
	EUL = eul()
	DUTY_PREV = 100
	DIFF_PREV = 0

	while abs(EUL - DES_EUL) > TOL_EUL:
		stuck = 0
		EUL = eul()
		print('Current Angle: {}' .format(EUL))
		DIFF = EUL - DES_EUL
		#INCREMENT = abs(DIFF/10)
		#if INCREMENT < 2: #min acc (to overcome static friction)
		#	INCREMENT = 2
		#elif INCREMENT > 10: #max acc (to avoid over-rotation)
		#	INCREMENT = 10
		if DIFF > 0: #direction to spin
			IO.output(DIR_CTRL, IO.HIGH)
		else:
			IO.output(DIR_CTRL, IO.LOW)
		#if abs(DIFF) < abs(DIFF_PREV): #slow/speed depending on change in angle
		#	DUTY = DUTY_PREV + INCREMENT
		#else:
		#	DUTY = DUTY_PREV - INCREMENT
		DUTY = 100 - abs(DIFF/2)
		if DUTY < 1:
			DUTY = 1
		elif DUTY > 100:
			DUTY = 100
		M.ChangeDutyCycle(DUTY)
		if DUTY == DUTY_PREV: #check that reoccuring angle is stuck, then shock system
			if stuck == 10:
				kick(DUTY)
				DUTY = 100
				DUTY_PREV = DUTY
				stuck = 0
		elif stuck > 0:
				stuck = stuck + 1
		else:
			stuck = 0
		#if DUTY < 5:
		#	desaturate(DUTY)
		#	DUTY = 100
		#DIFF_PREV = DIFF
		DUTY_PREV = DUTY
		time.sleep(0.005)
		#print(DUTY)

for x in range(50):
	EUL = eul()
	VEL = vel()
	if abs(EUL - DES_EUL) < TOL_EUL and abs(VEL) < TOL_VEL:
	#within all tolerances
		print('Within Range')
		continue
	elif abs(VEL) > TOL_VEL:
	#incorrect speed
		detumble()
	elif abs(EUL - DES_EUL) > TOL_EUL and abs(VEL) < TOL_VEL:
	#incorrect orientation, 'no' speed
		rotate()
	time.sleep(2.5)

M.stop()
IO.cleanup()
