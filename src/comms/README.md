# Mock Sat - Communications

The purpose of this repository is to keep track of work and issues while building the communication software for a working (non-flight ready) satellite.

## Implementation

Four files are required to operate the MOC-SAT Communications. These include:

1. ground_station.py
2. ground_station.ino

3. satellite.py
4. satellite.ino

### ground_station.py

Opens a GUI that enables the user to send various commands to the connected tranceiver. The GUI has a serial monitor that can read data received from the connected arduino through the serial connection.

Upload this script to a computer (base station) and change hardware settings under CONFIGURATION in file.

### ground_station.ino

The connected Arduino and radio receives command from GUI and implements the respected command. The Arduino first sends an OP_CODE to the satellite's transeiver and then waits to receive data from the satellite.

Upload this script to the arduino (base station) and change hardware settings under Hardware Config and Radio Config in file.

### satellite.py

Reads an OP_CODE from the connected transceiver and executs an instruction according to it.

Upload this script to a rasperryPi (satellite) and change hardware settings under CONFIGURATION in file.

### satellite.ino

The connected Arduino and radio receives command from the base station transeiver and forwards it to the OBC (satellite.py). The Arduino then transmits the data corresponding to the received OP_CODE to the ground station transeiver.

Upload this script to the arduino (satellite) and change hardware settings under Hardware Config and Radio Config in file.
