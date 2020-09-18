# Mock CubeSat - Communications

The purpose of this repository is to keep track of work and issues while building the communication software for a working (non-flight ready) satellite.

## Shake Hands

A basic program that ping-pongs a character to the arduino. Used to initially test serial port connection.

## pySerial_String

Fully functional code to generate a received.png from a sent.png. Program ping-pongs encoded img data using pySerial and the Arduino. Use as a reference for encoding and decoding data

## extract_pngs

Work In Progress. Expected use this program is for when working with OBC. Able to read a file and extract png images using the image signature for pngs.

## img_transeiver

Cleaned up version of pySerial_String. Able to encode png image file, send packet of 32 characters to Arduino, and have Arduino transmit to the receiver.

Sept 11 // Having trouble sending the same like multiple times. Unsure if it's a transmit or recieve issue.

Sept 12 // Working with different baurdrates. Changed everything to 115200. Checks need to be implemented in the future.

Sept 17 // Added in many debugging statements in subroutines. Changed main so that the next package sent will only occur with the acknowledgement from the arduino. Currently implemented with transeiver_test_tx.ino

## img_receiver

Sept 17 // Made the same changes as in img_transeiver. Currently can not successfully read correct response from Arduino. recvLikeArduino returns XXX constantly. Currently being implemented with transeiver_test_rx.ino
