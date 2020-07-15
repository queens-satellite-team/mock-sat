from time import sleep
import io
import serial
def main():
    ser = serial.Serial('/dev/ttyS8', 9600)
    while True:
        if ser.readline() == 'send\r\n':
            with open('../img/sent.jpg', 'rb') as image:
                buffer_size = 28 #bytes
                while True:
                    buffer = image.read(buffer_size)
                    if not buffer: break
                    ser.write(buffer)
                    print(buffer)
                    while (ser.readline() != 'ack\r\n'):
                        sleep(0.1)
                    sleep(0.4)
                    if ser.readline() == 'end\r\n': break

    '''
        with open('../img/sent.jpg', 'rb') as image:
            buffer_size = 32 #bytes
            while True:
                buffer = image.read(buffer_size)
                if not buffer: break
                ser.write(buffer)
                print(buffer)
                sleep(1)
    '''
if __name__ == '__main__':
    main()
