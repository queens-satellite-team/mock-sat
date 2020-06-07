# QSET - Satellite Team Subsystems

A CubeSat can be broken into six major subsystems: structure, communication, power, attitude determination and control, command and data handling, and the payload. In the past, QSAT has had an exec team of managers for each subsystem and a CTO. QSAT&#39;s goal is to create a CubeSat that can rotate itself and take pictures at given orientation. This involves designing and building each of the subsystems and the computer system that would connect them.

[More info on CubeSat Subsystems](https://www.fictiv.com/blog/posts/satellite-101-what-is-a-cubesat#:~:text=A%20CubeSat%20contains%20many%20components,data%20handling%2C%20and%20the%20payload.)

## ADCS – Attitude determination and Control System

&quot;_The attitude determination and control system (ADCS) controls the orientation of the CubeSat with respect to an inertial frame of reference and includes reaction wheels, magnetorquers, thrusters, star trackers, sun and Earth sensors, angular rate sensors and GPS receivers and antennas. This complex system is needed because when the satellite is first deployed, for example via NanoRacks from the International Space Station, it is tumbling. Some CubeSats can operate in this state, but others require pointing accuracy and location knowledge.&quot;_

During the first CSDC that Queen&#39;s participated in, the CubeSat only required passive attitude stabilization. (For this reason, the ADCS was just a couple long magnets.) The new ADCS requires active attitude actuation and momentum dumping. The current design includes a setup with 10 sun sensors, a BNO055 Absolute Orientation Sensor, 4 reaction wheels (1 redundant) and 3 magnetorquers. The goal is for the ADCS to provide precise attitude control with the reaction wheels and detumbling with the magnetorquers.

## _Comms – Ground to Sat Communications System_

&quot;_The communications system (COM) is severely limited by the amount of power available, which is usually around 2W. Compared to Boeing&#39;s 702SP Spacecraft, which uses a Xenon Electrostatic ion thruster system (XIPS), operates in the low- to mid-power range of satellites, and has three to eight kilowatts of power, CubeSats&#39; power is exponentially less._

_CubeSats use radio-communication systems in VHF, UHF, F-, S-, C- and X-band. The satellite uses an antenna, usually deployed once in orbit to help with communication. Antennas range from commercial measuring tape to more complicated inflatable dish antennas.&quot;_

## _EPS – Electrical Power System_

&quot;The electrical power system (EPS) consists of solar panels and batteries. Solar panels hold solar cells that convert the solar light from the sun to electricity. Batteries take up a lot of mass and volume on the already tightly packed CubeSat. A major design challenge is placing the solar panels, either on the sides of the CubeSat itself, or having deploying solar panels. Having deployable panels adds solar cell area but also an extra mechanical complexity. For the panels to deploy, they need a burn wire release mechanism, and every mechanical system adds the possibility of a failure. If the panel does not deploy properly, the CubeSat will not have any power and even if everything else is functioning properly, the CubeSat will fail due to the lack of power.&quot;

## _OBC – Onboard Computer System_

The OBC is the system that runs the CubeSat&#39;s software and connects and controls all the other subsystems. &quot;An OBC primarily consists of a microprocessor, memory banks and interfacing chip to connect the computer to other sub-systems.&quot;

Last year, most of the work and research on the OBC involved designing a system that was radiation hardened with redundant processors and bit voting logic. This was intended to rectify potential bit switching caused by ionizing radiation in LEO. Unfortunately, the complexity this created is beyond the scope of what QSAT is trying to accomplish this year, so the focus will be on creating a traditional OBC.

[More OBC info](https://blog.satsearch.co/2020-03-11-overview-of-on-board-computers-available-on-the-global-space-marketplace)

## _Payload – Camera and Telescope_

&quot;_The payload, or the purpose of the CubeSat, dramatically varies, depending on the type of mission required. These can include cameras for pictures or video, like Planet Labs, or space qualification of certain electronic components, testing of a flight control system, or even some type of biological experiment.&quot;_

QSAT&#39;s current mission is to create a satellite that can take pictures of the Earth. For this reason, the payload is essentially a camera sensor and a focusing lens. Pictures taken by the camera also need to be stored on the sat until they can be downlinked to the command station.
