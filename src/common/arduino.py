"""
arduino python interface class
~~~~~~~~~~~~

A library to facilitate communication between python scripts
and arduino microcontrollers. Provides basic communication 
methods for UART, I2C, and SPI protocols. For direct implementation,
the matching Arduino is expected to have the firmware file loaded on
to it from: mock-sat/firmware/common/arduino/arduino.ino
"""

import serial
from serial import SerialTimeoutException

class Arduino:
    """Arduino base class. This class can be inherited by a parent
    classes, i.e. one of the sub-system devices (radio, camera,
    etc.) that utilize an Arduino as its controller. The parent
    will have access to all methods defined here.
    """

    def __init__(self, port='/dev/ttyACM0', baud=115200, timeout=1) -> None:
        self.ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
        self.ser.reset_input_buffer()

    def send_over_serial(self, string:str='hello world'):
        ''' Send a message with serial (UART) communication.

        Params:
            - string: the data to send.

        Returns:
            - count (int): the number of bytes written.

        Raises:	
            - SerialTimeoutException: In case a write timeout is configured for the port and the time is exceeded.
        '''
        self.ser.flushOutput()
        count = 0
        try:
            count = self.ser.write(string.encode('utf-8'))
        except SerialTimeoutException as e:
            print(f'{self} failed to write over serial. Is the Arduino plugged in?')
            raise e
        return count

    def receive_over_serial(self):
        '''Read and return one line from the USB port.

        Params:
            - None
        
        Returns:
            - line (string): the data received from the USB port
                or "xxx" if no data is available.

        Raises:
            - None
        '''
        line = 'xxx'
        if self.ser.inWaiting() > 0:
            line = self.ser.readline().decode('utf-8').rstrip()
        return line

    def send_over_i2c(self):
        pass

    def receive_over_i2c(self):
        pass

    def send_over_spi(self):
        pass

    def receive_over_spi(self):
        pass