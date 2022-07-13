from ..common.arduino import Arduino
from ..common.logger import SatelliteLogger
import serial
from serial.serialutil import SerialException
import sys
import time
import base64

class Radio(Arduino):
    '''Interface class to control a radio.'''

    def __init__(self, uid, port, baud=115200, start_marker='<', end_marker='>'):
        super().__init__()
        self._uid = uid                                     # unique ID
        self.supported_modes = ['T', 'R']                   # transmit, receive
        self.logger = SatelliteLogger.get_logger('radio')   # for debug, info, warning, and critical messages

        self.__wait_for_msg('ready: serial')                # this message is expected to be received from the arduino firmware
        self.__set_uid()                                    # tell the arduino which radio you are using (0 or 1)
        self.__wait_for_msg('ready: radio')                 # this message is expected to be received from the arduino firmware
        self.logger.info(f'radio {uid} booted')             # info message for the user

    def transmit(self, data:str):
        '''Send a string of characters to the other radio, await for a response.

        Params:
            - data (str): 32 characters (string or bytes) to send.
        '''

        self._transmit_header(data)
        self.logger.debug(f'transmitted: {data}')
        got_back = self.receive()
        if got_back == 'xxx':
            self.logger.warning(f'failed to receive acknowledgement')
        self.logger.debug(f'received in return: {got_back}')

    def receive(self, timeout:float=60.0):
        '''Attempt to receive a single message from the other radio.

        Params:
            - timeout (float): duration in which to receive a message.

        Return:
            - if received, the string sent from the arduino over serial.
            - if not received, 'xxx'
        '''
        start_time = time.time()
        received = 'xxx'
        while received == 'xxx':
            received = self.receive_over_serial().strip()
            if time.time() > start_time + timeout:
                self.logger.warning(f'no message received within {timeout} s.')
                break
        return received

    def _transmit_header(self, data:str, mode:str='T', num_payloads:int=1):
        '''Send a single header message.

        Params:
            data (str): the header message to be transmitted to the other radio.
            mode (str): the mode to switch the radio to. Can be "T" or "S".
        Raises:
            ValueError: the radio can not transmit an empty message or a string greater
                        that 32 bytes long.
        Return:
            data_len (int): the number of characters transmitted.
        '''

        data_len = len(data)

        if not data: # must not be an empty string
            raise ValueError('passed in an empty string!')

        if data_len > 32: # max 32 bytes for a single transmission
            raise ValueError(f'string is too long, {data_len} is greater than 32 characters')

        formatted_data = self._format_header(mode, num_payloads, data)
        try:
            self.send_over_serial(formatted_data)
        except Exception as e:
            self.logger.error(f'failed to transmit: {formatted_data}')
            raise e

        return data_len

    def _format_header(self, mode:str, num_payloads:int, data:str):
        '''Formart the data to what the arduino expects for transmissions.

        Return:
            - formatted data string to be then called with _send_to_arduino
        '''
        mode = mode.upper()
        if mode not in self.supported_modes:
            raise IndexError(f'Using unsupported mode: {mode}, "T", "S", or "R" are expected.')

        return mode + ':' + str(num_payloads) + ':' + data

    def __set_uid(self):
        if self._uid not in [0, 1]:
            raise ValueError(f'uid must be 0 or 1, not {self._uid}')
        radio_number = str(self._uid)
        self.send_over_serial(radio_number)

    def __wait_for_msg(self, msg:str='ready: serial', timeout:int=10):
        start_time = time.time()
        incoming = ''
        while incoming.find(msg) == -1:
            if time.time() > start_time + timeout:
                self.logger.warning(f'no message received, expected: {msg}')
                break
            incoming = self.receive_over_serial()
            if not (incoming == 'xxx'):
                self.logger.debug(incoming)