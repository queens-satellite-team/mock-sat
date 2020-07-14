from time import sleep
import io
import serial
def main():
    ser = serial.Serial('/dev/ttyS8', 115200)
    with open('../img/sent.jpg', 'rb') as image:
        buffer_size = 32 #bytes
        while True:
            buffer = image.read(buffer_size)
            if not buffer: break
            ser.write(buffer)
            print(buffer)
            sleep(1)
if __name__ == '__main__':
    main()
