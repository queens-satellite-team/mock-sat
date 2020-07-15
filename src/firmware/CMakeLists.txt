add_subdirectory(examples)

generate_arduino_firmware(server
    SKETCH server.cpp
    PORT /dev/ttyS8
    SERIAL picocom @SERIAL_PORT@
    BOARD mega2560)

generate_arduino_firmware(client
    SKETCH client.cpp
    PORT /dev/ttyS9
    SERIAL picocom @SERIAL_PORT@
    BOARD mega2560)

generate_arduino_firmware(transmitter
    SKETCH transmitter.cpp
    PORT /dev/ttyS8
    SERIAL picocom @SERIAL_PORT@
    BOARD mega2560)

generate_arduino_firmware(receiver
    SKETCH receiver.cpp
    PORT /dev/ttyS9
    SERIAL picocom @SERIAL_PORT@
    BOARD mega2560)
