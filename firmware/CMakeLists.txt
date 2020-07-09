add_subdirectory(test)
generate_arduino_firmware(moc-sat
    SKETCH moc_sat.cpp
    PORT /dev/ttyS8
    SERIAL picocom @SERIAL_PORT@
    BOARD mega2560)

generate_arduino_firmware(base-station
    SKETCH base_station.cpp
    PORT /dev/ttyS9
    SERIAL picocom @SERIAL_PORT@
    BOARD mega2560)
