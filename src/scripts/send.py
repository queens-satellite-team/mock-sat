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
            sleep(0.2)
            print(buffer)
if __name__ == '__main__':
    main()
