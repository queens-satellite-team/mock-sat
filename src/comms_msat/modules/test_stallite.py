from pytest_mock import mocker
import serial
from satellite import setupSerial, SatelliteErrors

def test_setupSerial_serialPortSucceeds(mocker):
    # Mock serial.Serial method
    mocker.patch.object(serial, 'Serial')

    serialPort = setupSerial(serial, 9600, "/dev/ttyACM0")

    # Assert Serial was called with correct parameters
    serial.Serial.assert_called_with(port="/dev/ttyACM0",
                                     baudrate=9600,
                                     rtscts=True,
                                     timeout=0)

def test_setupSerial_serialPortFails(mocker):
    mocker.patch.object(serial, 'Serial')
    serial.Serial.side_effect = serial.SerialException()
    # Device is connected on /dev/ttyACM1  so /dev/ttyACM0 throws exception:
    assert setupSerial(serial, 9600, "/dev/ttyACM0") == SatelliteErrors.SERIAL_DEVICE_NOT_FOUND

    serial.Serial.side_effect = ValueError()
    # Device configuration fails because parameters are invalid
    assert setupSerial(serial, 19292020, "/dev/ttyACM0") == SatelliteErrors.SERIAL_PARAM_OUT_OF_RANGE

    serial.Serial.side_effect = OSError() # Example of unknown error that could occur
    # Device configuration fails because parameters are invalid
    assert setupSerial(serial, 19292020, "/dev/ttyACM0") == SatelliteErrors.UNKNOWN_ERROR
