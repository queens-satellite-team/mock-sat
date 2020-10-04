# Mock CubeSat - Communications

The purpose of this repository is to keep track of work and issues while building the communication software for a working (non-flight ready) satellite.

## Implementation

Four files are required to operate the moc-sat communications. These include:

1. Upload transeiver_text_3_tx.ino to one Arduino and RF24 radio setup on one computer, and upload transeiver_text_3_rx.ino to another Arduino and RF24 radio setup on another computer.
2. On the receiving computer, open img_receiver.py, change baudrates to 115200, and update the portname to work with your computer setup. Run the python module.
3. On the transmitting computer, open img_transmitter.py, change baudrates to 115200, and update the portname to work with your computer setup. Run the python module.
4. Progress update should be displayed in terminal, and data shall be being sent.

## extract_pngs

Work In Progress. Expected use of this program is for when working with OBC. Able to read a file and extract png images using the image signature for pngs.

## img_transeiver

Cleaned up version of pySerial_String. Able to encode png image file, send packet of 32 characters to Arduino, and have Arduino transmit to the receiver.

Sept 11 // Having trouble sending the same like multiple times. Unsure if it's a transmit or recieve issue.

Sept 12 // Working with different baurdrates. Changed everything to 115200. Checks need to be implemented in the future.

Sept 17 // Added in many debugging statements in subroutines. Changed main so that the next package sent will only occur with the acknowledgement from the arduino. Currently implemented with transeiver_test_tx.ino

Sept 26 // Unable to get the RF24 default library test files Basic_TX and BASIC_RX to work on Arduino. Data is sent by transmitter but no ACK is sent back, and an empty message is received.

Oct 5 // Working radio connection between Arduinos.
Solution: Swapped Arduino to which computer they were connected to.
Suspected Cuase: Due to the old bootloaders on the knock off Arduinos they only work with the computer they were original plugged into.
Next Steps: Takes about 2 mins to send and receive one 32-character packet. Computer goes to sleep before able finishing transmission. Speed up the process of the transmission and complete appendToString method in img_receiver.

## img_receiver

Sept 17 // Made the same changes as in img_transeiver. Currently can not successfully read correct response from Arduino. recvLikeArduino returns XXX constantly. Currently being implemented with transeiver_test_rx.ino

Sept 26 // Same as img_transmitter. Unable to get the RF24 default library test files Basic_TX and BASIC_RX to work on Arduino. Data is sent by transmitter but no ACK is sent pack, and an empty message is received.

Oct 2 // Updated stop condition for receiving img data packets from arduino instead of knowing the image size. Using 'STOP' as termination message.
