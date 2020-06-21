import time
import RPi.GPIO as IO
IO.setmode(IO.BCM)

IO.setwarnings(False)

IO.setup(26, IO.OUT)
p = IO.PWM(26, 35000)

IO.setup(3, IO.OUT)
IO.output(3, IO.HIGH)

p.start(90)
time.sleep(1)
p.stop()

IO.cleanup()
