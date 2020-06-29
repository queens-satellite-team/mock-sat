#generate_arduino_firmware(hello-world
#    SKETCH hello_world.cpp
#    PORT  /dev/ttyS8
#    SERIAL picocom @SERIAL_PORT@
#    BOARD mega2560)
#
#generate_arduino_firmware(test-sd-card
#    SKETCH test_sd_card.cpp
#    PORT  /dev/ttyS7
#    #HDRS ${ARDUINO_SDK_PATH}/libraries/SD/SD.h
#    #     ${ARDUINO_SDK_PATH}/libraries/SPI/SPI.h
#    SERIAL picocom @SERIAL_PORT@
#    BOARD mega2560)
#
#generate_arduino_firmware(test-i2c-master
#    SKETCH test_i2c_master.cpp
#    PORT  /dev/ttyS7
#    #HDRS ${ARDUINO_SDK_PATH}/libraries/Wire/Wire.h
#    SERIAL picocom @SERIAL_PORT@
#    BOARD mega2560)
#
#generate_arduino_firmware(test-i2c-slave
#    SKETCH test_i2c_slave.cpp
#    PORT  /dev/ttyS8
#    #HDRS ${ARDUINO_SDK_PATH}/libraries/Wire/Wire.h
#    SERIAL picocom @SERIAL_PORT@
#    BOARD mega2560)
generate_arduino_firmware(test-transceiver-transmit
    SKETCH test_transceiver_transmit.cpp
    PORT /dev/ttyS8
    SERIAL picocom @SERIAL_PORT@
    BOARD mega2560)

generate_arduino_firmware(test-transceiver-receiver
    SKETCH test_transceiver_receive.cpp
    PORT /dev/ttyS9
    SERIAL picocom @SERIAL_PORT@
    BOARD mega2560)
