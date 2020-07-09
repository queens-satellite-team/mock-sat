import os
import serial
import time
from PIL import Image
def Get32ByteBuffers(bytes):
    buffer = []
    for i in range(0, len(bytes), 32):
        buffer.append(bytes[i:i+32])
    return buffer

def main():
    print("------------------------------------------------------------------")
    print("|                        SIMULATED SD CARD                       |")
    print("------------------------------------------------------------------")
    prompt = raw_input("Press enter to send image to transciever: ")
    if prompt == "":
        print("Writing image...")
        with Image.open('./img/image.jpg') as image:
            print("Image opened.")
            with serial.Serial('/dev/ttyS8', 115200) as ser:
                print(ser.name+" opened.")
                #buffers = Get32ByteBuffers(image.tobytes())
                #for buffer_32_byte in buffers:
                print("Writing hello world")
                ser.write(b'Hello, World!')
        print("Done writing.")
    else:
        print("Not writing image.")

if __name__ == "__main__":
    main()
