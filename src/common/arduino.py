"""
arduino python interface class
~~~~~~~~~~~~

A library to facilitate communication between python scripts
and arduino microcontrollers. Provides basic communication 
methods for UART, I2C, and SPI protocols. For direct implementation,
the matching Arduino is expected to have the firmware file loaded on
to it from: mock-sat/firmware/common/arduino/arduino.ino
"""

class Arduino:
    """Arduino base class. This class can be inherited by a parent
    classes, i.e. one of the sub-system devices (radio, camera,
    etc.) that utilize an Arduino as its controller. The parent
    will have access to all methods defined here.
    """

    def __init__(self) -> None:
        pass

    def send_over_serial(s):
        pass

    def receive_over_serial():
        pass

    def send_over_i2c():
        pass

    def receive_over_i2c():
        pass

    def send_over_spi():
        pass

    def receive_over_spi():
        pass