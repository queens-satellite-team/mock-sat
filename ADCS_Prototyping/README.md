The following scripts rely on:
-the RPi.GPIO library for python control of raspi IO pins (often comes pre-installed on raspi)
-the adafruit_bno055 library (for reading BNO055 sensor)
-all other libraries should be installed with python3

`BNO055_TEST.py` 
-tests the i2c connection between the raspi and the BNO055 sensor (currently tested with DFRobot's Gravity BNO055 sensor)

`FIT0441_TEST.py`
-tests the PWM control of the FIT0441 motor + controller unit - note that PWM uses pin 18 as that is the only harware PWM pin on the raspi 3B+

`MAX_TRQ.py`
-generates maximum change in reaction wheel momentum - used to test viability of testing platform

`PID_TEST.py`	***DISCONTINUED***
-initial attempt at PROPORTIONAL control of satellite orientation (single axis) - discontinued due to faulty testing bed (1st iteration gimbal)

`P_TEST.py`	***DISCONTINUED***
-second attemp at PROPORTIONAL control of satellite orientation (single axis), attempted patches for faulty testing bed - discontinued due to dampening of testing bed (2nd iteration gimbal)

`PI_TEST.py`
-partially working PROPORTIONAL-INTERGRAL control of satellite orientation (single axis) - tested using string testing bed
