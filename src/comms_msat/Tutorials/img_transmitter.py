#!/usr/local/bin/python3

import serial
import sys
import time
import base64

startMarker = "<"
endMarker = ">"
dataStarted = False
dataBuf = ""
messageComplete = False
pack_size = 32
start = 0
stop = pack_size

# filename = str(sys.argv[1])
filename = "moc-sat/src/comms_msat/img/sent.png"
# portname = str(sys.argv[2])
portname = "/dev/cu.usbserial-1420"


def setupSerial(baudRate, serialPortName):

    global serialPort

    serialPort = serial.Serial(
        port=serialPortName, baudrate=baudRate, timeout=0, rtscts=True
    )

    print("Serial port " + serialPortName + " opened  Baudrate " + str(baudRate))

    waitForArduino()


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


def main():
    setupSerial(115200, portname)
    imageToCharacters(filename)

    # loop through entire utf-8 string.
    # We skip across string by the pack size as that many characters are sent at once over serial to the Arduino
    for i in img_chars[::pack_size]:

        # create a packet to send
        pack = createPack()

        # send the pack to Arduino over SPI
        sendToArduino(pack)

        # check for a reply
        arduinoReply = recvLikeArduino()

        print("Waiting for Arduino Response.")
        # wait until we get an acknowledgement
        while arduinoReply.find("XXX") == 0:

            if arduinoReply.find("Error") == 0:
                print(arduinoReply)
                arduinoReply = recvLikeArduino()
                continue
            elif arduinoReply.find("Success") == 0:
                print(arduinoReply)
                break
            elif arduinoReply.find(" ") == 0:
                arduinoReply = recvLikeArduino()
                continue
            # end_if

            time.sleep(0.01)
            arduinoReply = recvLikeArduino()
        # end_while

        print("Returned Message: {} at time {}.".format(arduinoReply, time.time()))
    # end_for

    sendToArduino("STOP")  # send stop message to inform an end of transmission


if __name__ == "__main__":
    main()
