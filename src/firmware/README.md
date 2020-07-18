# Firmware
This directory contains all source files related to Arduino development. The
build system that is being used is [Arduino CMake](https://github.com/queezythegreat/arduino-cmake).
If you would like to build the code, navigate to the /src directory.
```
mkdir build && cd build
cmake ..
make <name of executable>-upload
```
If you would like to monitor the serial port the executable was uploaded on, 
additionally run:
```
make <name of executable>-serial
```
To use the above command you must have [Picocom](https://linux.die.net/man/8/picocom)
installed. 

## Debugging
The `make <name of executable>-upload` command often fails with the dreaded:
```
avrdude: stk500v2_ReceiveMessage(): timeout
```
This means your system cannot communicate with the serial port that has been
specified, either it doesn't exist (i.e. nothing is plugged in) or another
device is blocking it. Make sure:
* You do not have the Arduino IDE open, this will block the serial port
* There are no other scripts or executables using the serial port
* The Arduino is plugged in
* You have permission to use this serial port on your system
If you are developing on Windows using WSLtty, the serial port can be finicky.
I would suggest following these [instructions](https://docs.microsoft.com/en-us/archive/blogs/wsl/serial-support-on-the-windows-subsystem-for-linux) and then uploading the "Hello World" serial writing example
using the Arduino IDE. Then you can confirm that the serial port is activated
and configured correctly. After that you should be able to build.

## Serial Monitoring
It can be useful to open a serial monitor. Since Arduino CMake requires Picocom,
it makes sense to use that. Modify the following command for your needs:
```
picocom -b 115200 -r -l /dev/ttyUSB0
```
To exit Picocom use <Ctrl-a><Ctrl-x>.
## Adding libraries
The build system will detect external libraries that you use if you install
them in `/usr/share/arduino/libraries`.
