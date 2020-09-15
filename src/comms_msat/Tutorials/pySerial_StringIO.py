from time import sleep
import base64
import serial

####################################################
### GLOBALS
####################################################
filename = "PythonAttempt/sent.png"
portname = "/dev/cu.usbserial-1410"
baudrate = 115200
tx_idx = 0
rx_idx = 0
start = 0
stop = 1
pack_size = 1
rx_string = ""
ready_msg = "Ready"
####################################################
### SUB_ROUTINES
####################################################


####################################################
### PROGRAM
####################################################

"""
Establish the connection on a specific port
TO DO: Make this into it's own function. Portable for Mac and Windows
"""
ser = serial.Serial(portname, baudrate)


with open(filename, "rb") as image:
    """
    encode bytes in file to base64 characters
    """
    img_encoded = base64.b64encode(image.read())
    nbytes = len(img_encoded)
    print("Encoded String {}".format(img_encoded))
    print("Encoded String Type: {}".format(type(img_encoded)))
    print("Encoded String Length: {}".format(nbytes))

    """
    Convert byte string to char string. 
    For testing purpose we compare this original string to the final string we receive from the Arduino. 
    In the Moc-Sat implementation this can't be done. 
    """
    char_string = img_encoded.decode("utf-8")
    nchars = len(char_string)
    print("Character String {}".format(char_string))
    print("Character String Type: {}".format(type(char_string)))
    print("Character String Length: {}".format(nchars))

    """
    Read ready string from arduino. For now, Arduino just sends a hardcoded "Ready" when it's done establishing a serial connection. 
    TO DO: Add in else statement for error handling 
    """
    ready_str = ser.readline().decode("utf-8")
    ready_str = ready_str.rstrip("\r\n")

    if ready_str == ready_msg:
        """
        Slice tring of bytes into smaller packets. 
        """
        for i in range(nchars):
            tx_pack = img_encoded[start:stop]
            print("Data Package Made: [{}] < {} >".format(tx_idx, tx_pack))
            # print("Data Package Type: {}.".format(type(tx_pack)))

            """
            Transmit data pack to Arduino
            """
            bytes_written = ser.write(tx_pack)

            if bytes_written == pack_size:
                print("Data Package Sent: [{}] <{}>".format(tx_idx, tx_pack))
                tx_idx += 1

                """
                Receive packets from arduino
                """
                rx_pack = ser.read(pack_size + 2)
                print("Data Package Received: [{}] <{}>".format(rx_idx, rx_pack))

                """
                Decode packet into str type. This is used so we may easily append each received character back into a copy of the original string.
                Data Received over serial from the Arduino has the return and newline charactes and must be removed to append to the final string. 
                """
                rx_pack = rx_pack.decode("utf-8")
                rx_pack = rx_pack.rstrip("\r\n")
                print("Decoded Data Package: [{}] {}".format(rx_idx, rx_pack))

                """
                Combine data packages into what will become the final string. 
                We also update the slice indices to move onto the next package. 
                """
                rx_idx += 1
                rx_string += rx_pack
                start += pack_size
                stop += pack_size
            else:
                print("Error: Bytes Not Written to Arduino!")

        # print("Received String: {}".format(rx_string))
        # print("Received String  {}.".format(type(rx_string)))

        if rx_string == char_string:
            """
            Convert char string back into ascii string.
            """
            byte_string = rx_string.encode("utf-8")
            # print("Byte String {}".format(byte_string))
            # print("Byte String Type: {}".format(type(byte_string)))

            """
            Convert ascii string into byte string
            """
            image_64_decode = base64.b64decode(byte_string)
            # print("Decoded String {}".format(image_64_decode))
            # print("Decoded String Type: {}".format(type(image_64_decode)))
            with open("received.png", "wb") as output:
                output.write(image_64_decode)
        else:
            print("Error: Returned String Does Not Match Transmitted String!")
    else:
        print("Error: Arduino Not Ready!")
