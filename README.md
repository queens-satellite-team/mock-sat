# Mock CubeSat

The purpose of this repository is to house all software and hardware required to build a Mock-Sat. A Mock-Sat is the Queen's Space Engineering Team - Satellite's hardware and software development platform. A typical use case for this platform is that you have some program or code idea and want to see how it interacts within the spacecraft system, or have some hardware and need to see how it can be integrated within the spacecraft system, you can build a moc-sat and implement your idea on top of the basic design.

## Mock-Sat Functionality

The moc-sat has the following resources are available to users:

- 1-axis orientation control
- image capturing
- one way communication (send beacon signals)

Additional resources to be worked on include:
- system configuration files
- simple two way communication
- command and data handling
- power generation and control
- fault detections
- fault responses
- multi-axis orientation control

## Mock-Sat Repository Layout

### Data Folder
This folder contains all images and text data on board the Moc-Sat. It is broken down into data that is to be sent out via the communications system, and data that is being stored either for testing

### Docs Folder
This folder contains general information and documentation regarding the moc-sat. This includes datasheets and papers that provide some additional theory behind the moc-sat.

### Firmware Folder
This folder contains all software to be put on seperate Arduino and STM32 microcontrollers that implement the different systems available to the moc-sat such as the communications system and the attitude determination and control system.

### Hardware Folder
This folder contains all hardware files, pinout, and wiring diagrams required to build the moc-sat systems.

### Media Folder
This folder contains all images used within this repository.

### SRC (Source) Folder
This folder contains all code written for the moc-sat on the raspberry pi. This includes python implementations for all sub-sytems and the actuall mock-sat itself.

### Tasks Folder
This folder contains all the tasks that the satellite is to perform. See the README instructions in the folder for creating new and how to use them!

# Getting Started
Below are the following steps to setup the software and hardware of the mock-sat.

## Software Setup
### Prerequisites
1. You should have python version 3.7 or greater installed.
2. The raspberry pi should have the latest version of the [Raspberry Pi OS (Buster)](https://www.raspberrypi.com/software/) installed.

You can see what version of python you are using with the following command in a terminal:
```
python3 -V
```

And you can determine which instance of python (as you can have multiple) you are running with the following command in a terminal:
```
which python3
```

### Setting up the Repository
Perform the following steps within a terminal.

1. Clone the repository.
```
git clone https://github.com/queens-satellite-team/mock-sat.git
cd mock-sat/
```

2. Create a python virtual environment. 
```
python3 -m venv moc-sat-venv
```

3. Activate the virtual environment and install all of the required packages.

- a. If you are on MacOS or Raspberry Pi (Linux):
```
source moc-sat-venv/bin/activate
moc-sat-venv/bin/python3 -m pip install --upgrade pip
moc-sat-venv/bin/pip3 install -r requirements.txt
```

- b. If you are developing on Windows:
```
source moc-sat-venv/Scripts/activate
moc-sat-venv/Scripts/python3 -m pip install --upgrade pip
moc-sat-venv/Scripts/pip3 install -r requirements.txt
```


## Hardware Setup
The following hardware is required:
- BLDC Motor, power supply, and motor controller.
- Two transceivers, one for the mock-sat and one for the ground station.
- Raspberry Pi
- Raspberry Pi Camera
- An orientation sensor (MPU650)
- Three Arduinos
- A 1-Axis test bed for the satellite

Please see the README.md in the hardware directory within this repository for further instructions.

## Google Drive 

- https://drive.google.com/drive/folders/1PjCpiJ1GjcGLUgqpvl0FE0fzke4_DoX0?usp=sharing

Meeting notes, logistical documents and other files that may not be in this repository are kept on a
[Google Drive](https://drive.google.com/drive/folders/1PjCpiJ1GjcGLUgqpvl0FE0fzke4_DoX0?usp=sharinghttps://www.google.com). The drive has public view access. If you are a member of QSAT and would like full edit access, please request access on the drive or send an email to joshua.wade@queensu.ca. Or just message me on facebook or something. 

## Repository Style Guidelines
In order to have consistency in the repository we are following the [Google
style guidelines](https://github.com/google/styleguide). The repository is 
primarily [C++](https://google.github.io/styleguide/cppguide.html) and 
[Python](https://google.github.io/styleguide/pyguide.html) but another relevant
style guideline is the [filetypes and names](https://developers.google.com/style/filenames).
If languages other than this are introduced into the repository, please consult
the associated style guideline and adhere to it.
