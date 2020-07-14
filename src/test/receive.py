from time import sleep
from io import BytesIO
import io
import serial
import sys, struct
from PIL import Image

ser = serial.Serial('/dev/ttyS9', 115200)

image_buffer = ''
count = 0
while True:
    byte = ser.readline()
    print(byte)
    file.write(byte)
