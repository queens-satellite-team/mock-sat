import serial
import time
import base64

startMarker = "<"
endMarker = ">"
dataStarted = False
dataBuf = ""
img_string = ""
messageComplete = False
outfile = "received.png"
portname = "COM3"


def setupSerial(baudRate, serialPortName):

    global serialPort

    serialPort = serial.Serial(
        port=serialPortName, baudrate=baudRate, timeout=0, rtscts=True
    )

    print("Serial Port " + serialPortName + " opened. Baudrate " + str(baudRate))

    waitForArduino()


def waitForArduino():

    print("Waiting for Arduino to Reset.")

    msg = ""
    while msg.find("Arduino is ready") == -1:
        msg = recvLikeArduino()
        if not (msg == "XXX"):
            print(msg)


def recvLikeArduino():

    global startMarker, endMarker, serialPort, dataStarted, dataBuf, messageComplete

    if serialPort.inWaiting() > 0 and messageComplete == False:
        x = serialPort.read().decode("utf-8")

        if dataStarted == True:
            if x != endMarker:
                # if we're not at the end yet append character to dataBuf
                dataBuf = dataBuf + x
            else:
                # when we get to the end update our checks
                dataStarted = False
                messageComplete = True
        elif x == startMarker:
            dataStarted = True
            dataBuf = ""

        if messageComplete == True:
            messageComplete = False
            return dataBuf
        else:
            return "XXX"


def sendToArduino(stringToSend):

    global startMarker, endMarker, serialPort

    stringWithMarkers = startMarker
    stringWithMarkers += stringToSend
    stringWithMarkers += endMarker

    serialPort.write(stringWithMarkers.encode("utf-8"))


def stringToImage(stringToDecode):

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


def main():
    # set up the serial connection made through the USB port to the Arduino
    setupSerial(115200, portname)

    # img_string starts off empty and gets appended to by the received data
    global img_string

    # receive the first packet
    arduinoReply = recvLikeArduino()

    # loop until we get the STOP message
    while arduinoReply.find("STOP") == -1:
        time.sleep(0.01)

        if arduinoReply.find("XXX") == 0:
            arduinoReply = recvLikeArduino()
            continue
        elif arduinoReply.find("Error") == 0:
            # if we receive an error, print the error, and try to get a new response
            print("Returned Message: {} at time {}.".format(arduinoReply, time.time()))
            arduinoReply = recvLikeArduino()
            continue
        elif arduinoReply.find("Success") == 0:
            # if we read success in the received packet, append it to the img_string
            img_string = img_string + arduinoReply
            print("Returned Message: {} at time {}.".format(arduinoReply, time.time()))
            arduinoReply = recvLikeArduino()
            continue
        else:
            # if we receive anything else, just try again.
            arduinoReply = recvLikeArduino()

        # end_while
    # end_while

    # after receiving all the data packets encode string back into img file
    stringToImage(img_string)


if __name__ == "__main__":
    main()
