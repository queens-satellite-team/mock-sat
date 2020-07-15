import serial
import time
def main():
    print("------------------------------------------------------------------")
    print("|                        BASE STATION                            |")
    print("------------------------------------------------------------------")
    with serial.Serial('/dev/ttyS9', 115200) as ser:
        with open("img/received_image.jpg", "w") as f:
            for i in range(0, 3319):
                f.write(ser.read(32))
                print(i, " read 32 bytes")
        print("received_image.jpg closed...")

if __name__ == "__main__":
    main()
