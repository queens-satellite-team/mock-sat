from time import sleep
import numpy as np
import io
import serial
import sys

ser = serial.Serial(
    "/dev/cu.usbserial-1410", 115200
)  # Establish the connection on a specific port

with open("PythonAttempt/img/sent.png", "rb") as img_file:
    img_file.seek(0, 2)  # seek the end
    num_bytes = img_file.tell()  # get the file size
    print(
        "Total Number of Bytes is: {}".format(num_bytes)
    )  # print out total bytes for user

    # return to the begining of the file
    img_file.seek(0, 0)
    rx_buffer = io.BytesIO()

    ready_byte = ser.readline()
    print(ready_byte)
    ser.flush()

    for i in range((num_bytes)):
        tx_bytes = img_file.read(1)
        print("Data Sent: {}".format(tx_bytes))
        ser.write(tx_bytes)
        sleep(0.1)
        rx_bytes = ser.readline()
        rx_buffer.write(rx_bytes)
        print("Data Received: {}".format(rx_bytes))

    with open("received.png", "wb") as outfile:
        png_data = rx_buffer.getvalue()
        outfile.write(png_data)
