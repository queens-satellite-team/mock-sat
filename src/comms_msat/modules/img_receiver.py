import serial
import time
import base64

startMarker = '<'
endMarker = '>'
dataStarted = False
dataBuf = ""
img_string = ""
messageComplete = False
outfile = "received.png"
portname = "COM3"
nchars = 16720


def setupSerial(baudRate, serialPortName):
    
    global serialPort

    serialPort = serial.Serial(port=serialPortName, baudrate=baudRate, timeout=0, rtscts=True)

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
    img_64_decoded = base64.b64decode(img_bytes)

    with open(outfile, mode = "wb") as output:
        output.write(img_64_decoded)
 
def main():
    setupSerial(115200, portname)

    global img_string

    while len(img_string) != nchars:
        arduinoReply = recvLikeArduino()
        if not (arduinoReply == "XXX"):
            img_string = img_string + arduinoReply
        
    stringToImage(img_string)


if __name__ == '__main__':
    main()