# Arduino-Pi comms testing

I'm currently working on reading files from the raspberry pi and sending to an arduino nano via serial port.

Serial comms between the pi and nanos is working, but needs to be made more robust.
The current nRF24 comms is happening with a simple transmit/receive data spam setup.
I've been testing using nRF24 ACK packets which seem to do the trick for bidirectional communication, just have to get it working properly and put all the pieces together.

It's taking a little longer than expected and the code is unorganized right now. I'll try to right a better setup guide and organize everything once it's all working
