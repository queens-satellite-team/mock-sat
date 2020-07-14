#! /usr/bin/python3
import argparse
import os, io
import serial
import time

def main():
    parser = argparse.ArgumentParser(\
        description='Send image to base station using an Arduino and\
                     NRF24L01 transceiver. Two Arduino\'s are required: one to\
                     send the image from and one to recieve it.')
    parser.add_argument(\
        '--send-on', metavar='/dev/ttyS*', type=str, required=True,\
        help='Port that the Arduino that will send the image is connected to,\
              for example: /dev/ttyS8, /dev/ttyS9')
    parser.add_argument(\
        '--receive-on', metavar='/dev/ttyS*', type=str, required=True,\
        help='Port that the Arduino that will recieve the image is connected to,\
              for example: /dev/ttyS8, /dev/ttyS9')
    parser.add_argument('-f', metavar='./img/*.jpg', type=str, required=True,\
        help='File path to image that should be sent.')
    args = parser.parse_args()
    print(args.send_on)
    print(args.receive_on)
    print(args.receive_on)
    print(args.f)

    print("\n-- Image -- ")
    print("Path: "+args.f)
    print("Size: "+str(os.path.getsize(args.f)/1000)+"Kb")


    bytes = io.BytesIO(open(args.f, 'rb').read())

    arduino_serial_buffer_size = 64 # bytes
    buffers = list(zip(*[iter(bytes.getvalue())]*arduino_serial_buffer_size))
    print(len(buffers))
    with serial.Serial(args.send_on, baudrate=115200) as ser:
        for i in range(0, 5):
            print(ser.write(i))


if __name__ == "__main__":
    main()
