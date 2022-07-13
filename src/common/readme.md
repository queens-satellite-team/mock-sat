# Common 
This folder contains all the common files that can be shared acrosss all sub-system code.

# 1.0 Arduino
The Arduino base class provides serial and i2c communication methods to be shared across any system. 

- More information on serial communication between a raspberry pi and an Arduino can be found [here](https://roboticsbackend.com/raspberry-pi-arduino-serial-communication/)
- More information on i2c communication between a raspberry pi and an Arduino can be found [here]()


## 1.1 Usage
We are leveraging Python's [class inheritance](https://www.w3schools.com/python/python_inheritance.asp) so that all our systems (radio, reaction wheel, etc.) can have the same communication method between the raspberry pi and the Arduino microcontrollers that implement the system. We can create a Python class that represents a system and inherent all methods from the Arduino class as seen below:

```
class Radio(Arduino):
    '''Radio sub-system to control an RF24 radio.
    '''

    def __init__(self):
        super().__init__()  # call the init function of the parent Arduino class
    
    def transmit(self, data:str):
        self.send_over_serial(data) # use the Arduino's class method to send over serial
```

## 1.2 Hardware Connections
Use the following image to setup the hardware connection between the raspberry pi and the Arduino.

### 1.2.1 Serial (USB)


### 1.2.2 Serial (GPIOs)


### 1.2.3 I2C (GPIOs)
Be careful during this step! Arduinos use 5V-logic and Raspberry Pis use 3V3-logic. Fortunatly, the Raspberry Pi has internal pull-up resistors on the I2C lines, which pull the bus up to 3.3-volts. As long as you don’t connect any devices that pull the levels up to 5-volts you will be OK. You should also note that Arduino has open-collector outputs. Because of this, the Arduino logic levels on its I2C bus will be set to the levels of the pull-ups, which in this arrangement are in the Raspberry Pi.


# 2.0 Satellite
This is our mock-sat python object. It reflects all the hardware capabilities of the mock-sat, and provides the functionality to control these hardware features. The mock-sat object is available to all tasks scheduled by the OBC task manager and can thus use all methods and attributes of the class. 

# 3.0 Logger
This is our main way to log and print out all debug, info, warning, and critical messages. This class prints messages to the terminal screen (stdout), and saves it to a log file called by defualt "logger.log". 


