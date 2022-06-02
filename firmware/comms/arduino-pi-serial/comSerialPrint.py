#!/usr/bin/env python3
import serial
import time
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()
    ser.write(b"Hello\n")

    while True:
        #the filepath is hardcoded for now
        ser.write(open("/home/pi/python-scripts/file.txt","rb").read())
        #max length of transmitted line is 32 chars
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)