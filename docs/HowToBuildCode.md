### Arduino Code
The Arduino code uses the [Arduino CMake](https://github.com/queezythegreat/arduino-cmake)
build system. To make sure the build system is working correctly perform the
following:
#### Linux
* Install CMake and the Arduino SDK. Install `picocom` if you do not already
  have it by running `sudo apt install picocom`. `picocom` is the default
  serial monitor for the build system.
* Connect an Arduino Mega 2560 to your computer. If you are going to connect
  a different Arduino, you must edit the `BOARD` parameter in
  `test/CMakeLists.txt` to reflect the Arduino you are using. If the Arduino
  is using a port other than `/dev/ttyACM0` you must change the `PORT` parameter
  in the same file.
* In the root of the repository, run the following commands:
  ```
  mkdir build && cd build    # create a build directory
  cmake ..                   # run CMake on the parent CMakeLists.txt
  make upload                # upload the firmware to the Arduino
  make hello_world-serial    # run a Picocom terminal to monitor the serial port
  ```
  You should see `Hello World!` being printed every second. To exit the picocom
  terminal, press Ctrl-a Ctrl-x.
