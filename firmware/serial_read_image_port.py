import serial

def main():
    with serial.Serial('/dev/ttyS8', 115200) as ser:
        print(ser.readline())

if __name__ == "__main__":
    main()
