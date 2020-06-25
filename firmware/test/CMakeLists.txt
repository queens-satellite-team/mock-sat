generate_arduino_firmware(hello_world
    SKETCH hello_world.cpp
    PORT  /dev/ttyS7
    SERIAL picocom @SERIAL_PORT@
    BOARD mega2560)
