import serial
from time import sleep
def checksum(buffer):
    return chr(sum([ord(c) for c in buffer])/256)

def main():
    with serial.Serial('/dev/ttyS9', 9600) as ser:
        start = b'0xC0\n'
        while True:
            if ser.readline() == start:
                print("Start transmission")
                msg = b'0xC0\n'
                buffer = b'bytes\n'
                msg += buffer + checksum(buffer) + b'\n'
                serial.write(msg)
                resend = b'0xC8\n'
                if ser.readline() == resend:
                    print("Not received")


if __name__ == '__main__':
    main()
