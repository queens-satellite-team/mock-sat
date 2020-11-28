"""
QSAT Communications Team 

The main objective of this module includes: 
    1. To have a GUI to choose from a list of commands 
    2. Easy communication to a connected Transmitting Radio (Arduino and RF24, or STM32 and CC1120)
    3. See progress of incoming data and have a log of previously sent commands and received data. 
"""
####################################################################
########################### USER CONFIG ############################
####################################################################

infile = "/moc-sat/src/comms_msat/imgs/sent.png"
outfile = "/moc-sat/src/comms_msat/imgs/received.png"
portname = "/dev/ttyACM0"  # for arduino uno on raspberryPi

####################################################################
############################# IMPORTS ##############################
####################################################################
from datetime import datetime
import serial
import sys
import time
import base64

####################################################################
############################# GLOBALS ##############################
####################################################################
startMarker = "<"
endMarker = ">"
dataStarted = False
newCMD = False
dataBuf = ""
img_string = ""
messageComplete = False
pack_size = 32
start = 0
stop = pack_size

####################################################################
####################### CONTROL SUBROUTINES ########################
####################################################################
def setupSerial(baudRate, serialPortName):

    global serialPort

    serialPort = serial.Serial(
        port=serialPortName, baudrate=baudRate, timeout=0, rtscts=True
    )

    print("Serial port " + serialPortName + " opened  Baudrate " + str(baudRate))

    waitForArduino()


def arduinoACK():
    msg = ""
    while msg.find("XXX") == 0:
        msg = recvLikeArduino()
        if msg == "success":
            print(msg)
            return True
        elif msg == "failed":
            print(msg)
            return False


def waitForArduino():

    # wait until the Arduino sends 'Arduino is ready' - allows time for Arduino reset
    # it also ensures that any bytes left over from a previous message are discarded

    print("Waiting for Arduino to Reset...")

    msg = ""
    while msg.find("Arduino is ready") == -1:
        msg = recvLikeArduino()
        if not (msg == "XXX"):
            print(msg)


def recvLikeArduino():

    global startMarker, endMarker, serialPort, dataStarted, dataBuf, messageComplete

    if serialPort.inWaiting() > 0 and messageComplete == False:
        x = serialPort.read().decode("utf-8")  # decode needed for Python3
        x = x.rstrip("\r\n")

        if dataStarted == True:
            if x != endMarker:
                dataBuf = dataBuf + x
            else:
                dataStarted = False
                messageComplete = True
        elif x == startMarker:
            dataBuf = ""
            dataStarted = True

    if messageComplete == True:
        messageComplete = False
        return dataBuf
    else:
        return "XXX"


def sendToArduino(stringToSend):

    # this adds the start- and end-markers before sending
    global startMarker, endMarker, serialPort

    stringWithMarkers = startMarker
    stringWithMarkers += stringToSend
    stringWithMarkers += endMarker

    if serialPort.write(stringWithMarkers.encode("utf-8")):  # encode needed for Python3
        print("Success: Sent a packet to Arduino.")
    else:
        print("Error: Could not write to Arduino.")


def imageToCharacters(file):

    # encode bytes in file to base64 characters
    global img_chars, nchars

    with open(file, mode="rb") as image:
        img_encoded = base64.b64encode(image.read())
        if img_encoded:
            print("Image file successfully encoded.")
        else:
            print("Error: image file did not encode.")

        img_chars = img_encoded.decode("utf-8")
        if img_chars:
            print("Encoded image succefullly converted to utf-8 string.")
        else:
            print("Error: Encoded image did not convert to utf-8 string.")

        nchars = len(img_chars)
        print("Encoded Image is " + str(nchars) + " characters long.")


def charactersToImage(stringToDecode):

    global outfile

    img_bytes = stringToDecode.encode("utf-8")
    if img_bytes:
        print("Success: stringToImage: ASCII character string encoded to byte string.")
        img_64_decoded = base64.b64decode(img_bytes)

        if img_64_decoded:
            print("Success: stringToImage: Byte string decoded with base 64.")

            with open(outfile, mode="wb") as output:
                output.write(img_64_decoded)
                print("Ouput file: {} created.".format(outfile))
        else:
            print("Error: stringToImage: Byte string unable to decode with base 64.")
    else:
        print("Error: stringToImage: Character string not converted to bytes string.")


def createPack():

    global img_chars, start, stop, pack_size

    pack = img_chars[start:stop]

    if pack:
        print("Success: Pack succesfully created.")
        start += pack_size
        stop += pack_size
    else:
        print("Error: pack not created.")
        return

    return pack


def sendImage():
    pass


def sendHealthData():
    pass


def sendRebootConfirmation():
    pass


def cmd_one():
    """
    This command receives an image from the satellite's memory.
    The OP_code sent to the satellite is 1 and the angle given is attached to the command packet
    """
    pass


def cmd_two(self):
    """
    This command gets the health values from a text file on the satellite
    The OP_code being sent is 2 and no other information is required to be sent along. 
    """

    pass


def cmd_three(self):
    """
    This command reboots the satellite in case of a required update or to reestablish a connection. 
    For now, we are blinking LEDs on the satellite to confirm recognition. 
    The OP_code being sent is 3 and no other information is required to be sent along. 
    """
    pass


####################################################################
########################## MAIN WINDOW #############################
####################################################################
def main():
    setupSerial(9600, portname)

    global img_string

    msg = ""
    while msg.find("STOP") == -1:
        msg = recvLikeArduino()
        if not (msg == "XXX"):
            img_string += msg
            print(img_string)

    charactersToImage(img_string)
    print("Main Finished")


if __name__ == "__main__":
    main()
