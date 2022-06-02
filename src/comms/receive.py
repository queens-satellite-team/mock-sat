import serial
from time import sleep
def checksum(buffer):
    return chr(sum([ord(c) for c in buffer])/256)

def main():
    with serial.Serial('/dev/ttyS8', 9600) as ser:
        start = b'0xC0\n'
        ser.write(start)
        if ser.readline() == start:
            print("Receiving bytes")
            buffer = ser.readline()
            check1 = ser.readline()
            check2 = checksum(buffer)
            if check1 != check2:
                resend = b'0xC8\n'
                ser.write(resend)
            else:
                print(buffer)


if __name__ == '__main__':
    main()
