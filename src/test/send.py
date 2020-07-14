from time import sleep
import serial
ser = serial.Serial('/dev/ttyS8', 115200) # Establish the connection on a specific port
counter = 32 # Below 32 everything in ASCII is gibberish
while True:
    counter +=1
    ser.write(str(chr(counter))) # Convert the decimal number to ASCII then send it to the Arduino
    print ser.readline() # Read the newest output from the Arduino
    if counter == 255:
        counter = 32
