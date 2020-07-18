add_subdirectory(examples)

generate_arduino_firmware(transceiver-S8
    SKETCH transceiver.cpp
    PORT /dev/ttyS8
    SERIAL picocom @SERIAL_PORT@
    BOARD mega2560)

generate_arduino_firmware(transceiver-S9
    SKETCH transceiver.cpp
    PORT /dev/ttyS9
    SERIAL picocom @SERIAL_PORT@
    BOARD mega2560)

#generate_arduino_firmware(client
#    SKETCH client.cpp
#    PORT /dev/ttyS9
#    SERIAL picocom @SERIAL_PORT@
#    BOARD mega2560)
