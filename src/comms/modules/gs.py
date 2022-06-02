####################################################################
########################### USER CONFIG ############################
####################################################################

outfile = "/moc-sat/src/comms_msat/imgs/received.png"
infile = "moc-sat/src/comms_msat/imgs/sent.png"
portname = "/dev/cu.usbserial-1410"  # for arduino nano on mac

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
pack_size = 20
start = 0
stop = pack_size

####################################################################
####################### FLAGS and OP-CODES #########################
####################################################################
FLAG_DATA = 0
FLAG_COMMAND = 1

OP_CODE_CMD_ONE = 1
OP_CODE_CMD_TWO = 2
OP_CODE_CMD_THREE = 3

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


def stringToImage(stringToDecode):

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


def createPack(flag="NA", op_code="NA", length="NA", data="NA"):

    pack = str(flag)
    pack += str(op_code)
    pack += str(length)
    pack += data

    print(pack)

    return pack


####################################################################
########################## MAIN WINDOW #############################
####################################################################
def main():

    global start, stop

    setupSerial(9600, portname)

    imageToCharacters(infile)

    for i in range(4):
        img_data = img_chars[start:stop]
        start += pack_size
        stop += pack_size

        # data_pack = createPack(FLAG_DATA, OP_CODE_CMD_ONE, pack_size, img_data)

        sendToArduino(img_data)

        """ check for a reply """
        arduinoReply = recvLikeArduino()

        print("Waiting for Arduino Response.")
        # wait until we get an acknowledgement
        while arduinoReply.find("XXX") == 0:

            if arduinoReply.find("failed") == 0:
                print(arduinoReply)
                arduinoReply = recvLikeArduino()
                continue
            elif arduinoReply.find("success") == 0:
                print(arduinoReply)
                break
            elif arduinoReply.find(" ") == 0:
                arduinoReply = recvLikeArduino()
                continue
            # end_if

            arduinoReply = recvLikeArduino()
        # end_while

    # end_for

    # data_pack = createPack(FLAG_DATA, OP_CODE_CMD_ONE, pack_size, "STOP")
    sendToArduino("STOP")


if __name__ == "__main__":
    main()

