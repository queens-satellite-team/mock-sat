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
#### WSLtty
WSLtty does offer support for communicating with hardware through serial ports.
WSL automatically maps the `COM<N>` ports on Windows to `/dev/ttyS<N>` ports. 
For example, `COM7` would be mapped to `/dev/ttyS7`. You can check which `COM`
port is being used by going into `Device Manager` and checking the 
`Ports (COM & LPT)` header in Windows. If the port being used is `COM7`, then
you must run:
```
sudo chmod 666 /dev/ttyS7
```
then follow the instructions for Linux. Check [this](https://docs.microsoft.com/en-us/archive/blogs/wsl/serial-support-on-the-windows-subsystem-for-linux) for more information.
