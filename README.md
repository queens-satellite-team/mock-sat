# Mock CubeSat

The purpose of this repository is to house all software and hardware required to build a Mock-Sat. A Mock-Sat is the Queen's Space Engineering Team - Satellite's hardware and software development platform. 

## Mock-Sat Functionality

The moc-sat should be able to orient in one direction, take a photo, send the compressed image to a mock base station using the transceiver. This is based on the mission requirements from [CSDC-5](http://www.csdcms.ca/). The minimum requirements to satisfy this functionality are:

- R1. From an initial position set by the tester, the reaction wheel can rotate the satellite in the plane of the table so the camera points towards an image.
- R2. When the camera is aligned toward the image, a photo is taken.
- R3. The photo is stored on the OBC and sent by the transceiver to the base station.

## Mock-Sat Repository Layout

### Data Folder

### Docs Folder

### Firmware Folder

### Hardware Folder

### SRC (Source) Folder


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

3. Activate the virtual environment.
    a. If you are on MacOS or Raspberry Pi (Linux):
```
source moc-sat-venv/bin/activate
```

    b. If you are developing on Windows:
```
source moc-sat-venv/Scripts/activate
```

4. Install all of the required packages.
```
moc-sat-venv/bin/python3 -m pip install --upgrade pip
moc-sat-venv/bin/pip3 install -r requirements.txt
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
