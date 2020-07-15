generate_arduino_firmware(hello-world
    SKETCH hello-world.cpp
    PORT  /dev/ttyS8
    SERIAL picocom @SERIAL_PORT@
    BOARD mega2560)

generate_arduino_firmware(sd-card
    SKETCH sd-card.cpp
    PORT  /dev/ttyS7
    #HDRS ${ARDUINO_SDK_PATH}/libraries/SD/SD.h
    #     ${ARDUINO_SDK_PATH}/libraries/SPI/SPI.h
    SERIAL picocom @SERIAL_PORT@
    BOARD mega2560)

generate_arduino_firmware(i2c-master
    SKETCH i2c-master.cpp
    PORT  /dev/ttyS7
    #HDRS ${ARDUINO_SDK_PATH}/libraries/Wire/Wire.h
    SERIAL picocom @SERIAL_PORT@
    BOARD mega2560)

generate_arduino_firmware(i2c-slave
    SKETCH i2c-slave.cpp
    PORT  /dev/ttyS8
    #HDRS ${ARDUINO_SDK_PATH}/libraries/Wire/Wire.h
    SERIAL picocom @SERIAL_PORT@
    BOARD mega2560)
generate_arduino_firmware(transceiver-transmit
    SKETCH transceiver-transmit.cpp
    PORT /dev/ttyS8
    SERIAL picocom @SERIAL_PORT@
    BOARD mega2560)

generate_arduino_firmware(transceiver-receiver
    SKETCH transceiver-receive.cpp
    PORT /dev/ttyS9
    SERIAL picocom @SERIAL_PORT@
    BOARD mega2560)

generate_arduino_firmware(radiohead-nrf24-client
    SKETCH radiohead-nrf24-client.cpp
    PORT /dev/ttyS8
    SERIAL picocom @SERIAL_PORT@
    BOARD mega2560)

generate_arduino_firmware(radiohead-nrf24-server
    SKETCH radiohead-nrf24-server.cpp
    PORT /dev/ttyS9
    SERIAL picocom @SERIAL_PORT@
    BOARD mega2560)
