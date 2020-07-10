# Mock CubeSat

The purpose of this repository is to keep track of work and issues while building a working (non-flight ready) satellite.  

## Summer 2020 Goals

### Building Moc Sat
Over the summer, our team plans to quickly design and build a Mock Satellite with relatively cheap and non-flight ready components. The goal is to create a learning model that meets the minimum mission requirements and can be easily fixed and upgraded. For a more detailed description of the Summer Team Goals, see the summer team [discussion Post](https://github.com/orgs/queens-satellite-team/teams/summer/discussions/3).

### Facilitate transitions and plan for the year

Due to the effects of Covid-19, the QSAT transition period moving into 2020-2021 was cut short. This means that we'll need to find exec members for each subsystem and get documents and work from past exec. Once we have a team put together, we can plan out our goals for the year and create a budget plan.

- [Subsystem Information](https://drive.google.com/file/d/1AzUVqYonok9aeZg2w4fLos2Mheti_4PH/view?usp=sharing)

- [Exec Application Form](https://drive.google.com/file/d/1qkJ8QkFzmjUwb09uiYismIzTTNGWLFOD/view?usp=sharing)

## Moc-sat minimum requirements

The moc-sat should be able to orient in one direction, take a photo, send the compressed image to a mock base station using the transceiver. This is based on the mission requirements from [CSDC-5](http://www.csdcms.ca/). The minimum requirements to satisfy this functionality are:

- R1. From an initial position set by the tester, the reaction wheel can rotate the satellite in the plane of the table so the camera points towards an image.
- R2. When the camera is aligned toward the image, a photo is taken.
- R3. The photo is stored on the OBC and sent by the transceiver to the base station.

The following hardware is required:
- BLDC Motor, power supply, and motor controller.
- Two transceivers, one for the moc-sat and one for the base station.
- Raspberry Pi
- Raspberry Pi Camera
- An orientation sensor
- An Arduino
- A 1-Axis test bed for the satellite

## Google Drive 

- https://drive.google.com/drive/folders/1PjCpiJ1GjcGLUgqpvl0FE0fzke4_DoX0?usp=sharing

Meeting notes, logistical documents and other files that may not be in this repository are kept on a
[Google Drive](https://drive.google.com/drive/folders/1PjCpiJ1GjcGLUgqpvl0FE0fzke4_DoX0?usp=sharinghttps://www.google.com). The drive has public view access. If you are a member of QSAT and would like full edit access, please request access on the drive or send an email to joshua.wade@queensu.ca. Or just message me on facebook or something. 