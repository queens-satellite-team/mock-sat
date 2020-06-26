generate_arduino_firmware(hello-world
    SKETCH hello_world.cpp
    PORT  /dev/ttyS7
    SERIAL picocom @SERIAL_PORT@
    BOARD mega2560)

generate_arduino_firmware(test-sd-card
    SKETCH test_sd_card.cpp
    PORT  /dev/ttyS7
    HDRS ${ARDUINO_SDK_PATH}/libraries/SD/SD.h
         ${ARDUINO_SDK_PATH}/libraries/SPI/SPI.h
    SERIAL picocom @SERIAL_PORT@
    BOARD mega2560)
