import time
import RPi.GPIO as IO
IO.setmode(IO.BCM)

IO.setwarnings(False)

IO.setup(18, IO.OUT)
p = IO.PWM(18, 100)

IO.setup(15, IO.OUT)
IO.output(15, IO.HIGH)

p.start(100)
for x in range(100):
	time.sleep(0.1)
	p.ChangeDutyCycle(x)

p.stop()
IO.cleanup()
