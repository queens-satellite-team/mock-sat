# CMake rules for building examples
#generate_arduino_firmware(hello-world
#    SKETCH hello-world.cpp
#    PORT  /dev/ttyS8
#    SERIAL picocom @SERIAL_PORT@
#    BOARD mega2560)
#
#generate_arduino_firmware(test-sd-card
#    SKETCH test-sd-card.cpp
#    PORT  /dev/ttyS7
#    #HDRS ${ARDUINO_SDK_PATH}/libraries/SD/SD.h
#    #     ${ARDUINO_SDK_PATH}/libraries/SPI/SPI.h
#    SERIAL picocom @SERIAL_PORT@
#    BOARD mega2560)
#
#generate_arduino_firmware(test-i2c-master
#    SKETCH test-i2c-master.cpp
#    PORT  /dev/ttyS7
#    #HDRS ${ARDUINO_SDK_PATH}/libraries/Wire/Wire.h
#    SERIAL picocom @SERIAL_PORT@
#    BOARD mega2560)
#
#generate_arduino_firmware(test-i2c-slave
#    SKETCH test-i2c-slave.cpp
#    PORT  /dev/ttyS8
#    #HDRS ${ARDUINO_SDK_PATH}/libraries/Wire/Wire.h
#    SERIAL picocom @SERIAL_PORT@
#    BOARD mega2560)
#generate_arduino_firmware(test-transceiver-transmit
#    SKETCH test-transceiver-transmit.cpp
#    PORT /dev/ttyS8
#    SERIAL picocom @SERIAL_PORT@
#    BOARD mega2560)

#generate_arduino_firmware(test-transceiver-receiver
#    SKETCH test-transceiver-receive.cpp
#    PORT /dev/ttyS9
#    SERIAL picocom @SERIAL_PORT@
#    BOARD mega2560)
