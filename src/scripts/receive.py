from time import sleep
from io import BytesIO
import io
import serial
import sys, struct
from PIL import Image

ser = serial.Serial('/dev/ttyS9', 115200)
ser.flush()
with open('../img/received.jpg', 'wb') as file:
    while True:
        byte = ser.read()
        print(byte)
        file.write(byte)
