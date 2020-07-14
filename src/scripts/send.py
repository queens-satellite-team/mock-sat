from time import sleep
import io
import serial
ser = serial.Serial('/dev/ttyS8', 115200)

bytes = io.BytesIO(open('../img/sent.jpg', 'rb').read())

arduino_serial_buffer_size = 64 # bytes
buffers = list(zip(*[iter(bytes.getvalue())]*arduino_serial_buffer_size))

for buffer in buffers:
    for char in buffer:
        ser.write(str(char))
