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

## Adding libraries
The build system will detect external libraries that you use if you install
them in `/usr/share/arduino/libraries`.
