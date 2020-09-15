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
# filename = str(sys.argv[1])
filename = "PythonAttempt/img/sent.png"
# portname = str(sys.argv[2])
portname = "/dev/cu.usbserial-1410"


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

    print("Waiting for Arduino to Reset")

    msg = ""
    while msg.find("Arduino is ready") == -1:
        msg = recvLikeArduino()
        if not (msg == "XXX"):
            print(msg)


def recvLikeArduino():

    global startMarker, endMarker, serialPort, dataStarted, dataBuf, messageComplete

    if serialPort.inWaiting() > 0 and messageComplete == False:
        x = serialPort.read().decode("utf-8")  # decode needed for Python3

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

    serialPort.write(stringWithMarkers.encode("utf-8"))  # encode needed for Python3


def imageToCharacters(file):

    # encode bytes in file to base64 characters
    global img_chars, nchars

    with open(file, mode="rb") as image:
        img_encoded = base64.b64encode(image.read())
        img_chars = img_encoded.decode("utf-8")
        nchars = len(img_chars)


def main():
    setupSerial(115200, portname)
    imageToCharacters(filename)

    pack_size = 32
    start = 0
    stop = pack_size
    prevTime = time.time()

    for i in img_chars[start:stop:pack_size]:
        # check for a reply
        arduinoReply = recvLikeArduino()
        if not (arduinoReply == "XXX"):
            print("Time: %s  Reply: %s" % (time.time(), arduinoReply))

        # send a message at intervals
        if time.time() - prevTime > 1.0:
            sendToArduino(i)
            prevTime = time.time()
            start += pack_size
            stop += pack_size


if __name__ == "__main__":
    main()
