/**********************************************************************
* Copyright (C) 2016 Maxim Integrated Products, Inc., All Rights Reserved.
*
* Permission is hereby granted, free of charge, to any person obtaining a
* copy of this software and associated documentation files (the "Software"),
* to deal in the Software without restriction, including without limitation
* the rights to use, copy, modify, merge, publish, distribute, sublicense,
* and/or sell copies of the Software, and to permit persons to whom the
* Software is furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included
* in all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
* OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
* MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
* IN NO EVENT SHALL MAXIM INTEGRATED BE LIABLE FOR ANY CLAIM, DAMAGES
* OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
* ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
* OTHER DEALINGS IN THE SOFTWARE.
*
* Except as contained in this notice, the name of Maxim Integrated
* Products, Inc. shall not be used except as stated in the Maxim Integrated
* Products, Inc. Branding Policy.
*
* The mere transfer of this software does not imply any licenses
* of trade secrets, proprietary technology, copyrights, patents,
* trademarks, maskwork rights, or any other form of intellectual
* property whatsoever. Maxim Integrated Products, Inc. retains all
* ownership rights.
**********************************************************************/


#ifndef _MAX113XX_PIXI_H_
#define _MAX113XX_PIXI_H_


#include "mbed.h"
#include "MAX11301Hex.h"


/**
@brief MAX113XX - PIXI, 20/12-Port Programmable Mixed-Signal I/O with 
12-Bit ADC, 12-Bit DAC, Analog Switches, and GPIO

The MAX113XX family integrates a PIXI™, 12-bit, multichannel, analog-to-digital 
converter (ADC) and a 12-bit, multichannel, buffered digital-to-analog 
converter (DAC) in a single integrated circuit (IC). These devices offers 
20/12 mixed-signal high-voltage, bipolar ports, which are configurable as an 
ADC analog input, a DAC analog output, a general-purpose input port (GPI), 
a general-purpose output port (GPO), or an analog switch terminal. 
One internal and two external temperature sensors track junction and 
environmental temperature, respectively. Adjacent pairs of ports are 
configurable as a logic-level translator for open-drain devices or an 
analog switch.

Use configuration software found at
https://www.maximintegrated.com/en/products/analog/data-converters/analog-to-digital-converters/MAX11300.html/tb_tab2
to generate MAX113XXHex.h file
*/
class MAX113XX_Pixi
{
    public:
    
    ///Pixi devices
    enum Device_e
    {
        ///20 Port SPI
        MAX11300 = 0,
        ///20 Port I2C
        MAX11301,
        ///12 Port SPI
        MAX11311,
        ///12 Port I2C
        MAX11312
    };
    
    ///MAX113XX Ports
    enum Ports_e
    {
        PORT0 = 0,
        PORT1,
        PORT2,
        PORT3,
        PORT4,
        PORT5,
        PORT6,
        PORT7,
        PORT8,
        PORT9,
        PORT10,
        PORT11,
        PORT12,
        PORT13,
        PORT14,
        PORT15,
        PORT16,
        PORT17,
        PORT18,
        PORT19
    };
    
    ///MAX113XX Port Modes
    enum PortModes_e
    {
        ///HIGH_Z
        MODE_0 = 0,
        ///Digital input with programmable threshold, GPI 
        MODE_1,
        ///Bidirectional level translator terminal
        MODE_2,
        ///Register-driven digital output with DAC-controlled level, GPO
        MODE_3,
        ///Unidirectional path output with DAC-controlled level, GPO 
        MODE_4,
        ///Analog output for DAC
        MODE_5,
        ///Analog output for DAC with ADC monitoring
        MODE_6,
        ///Positive analog input to single-ended ADC
        MODE_7,
        ///Positive analog input to differential ADC
        MODE_8,
        ///Negative analog input to differential ADC
        MODE_9,
        ///Analog output for DAC and negative analog input to differential ADC
        MODE_10,
        ///Terminal to GPI-controlled analog switch
        MODE_11,
        ///Terminal to register-controlled analog switch
        MODE_12
    };
    
    ///ADC Conversion Modes
    enum ADCConversionModes_e
    {
        ///The ADC does not perform any conversion
        Idle = 0,
        ///The ADC sweeps through all ADC converted ports once on cnvt
        SingleSweep,
        ///The ADC does a single conversion for the current port in the sequence
        ///of ADC configured ports.  Must keep track of which port was last and
        ///how many ADC configured ports
        SingleConversion,
        ///ADC continuously sweeps through configured ports, cnvt isn't used
        ContinuousSweep
    };
    
    ///DAC operational modes
    enum DACModes_e
    {
        ///DAC configured ports are updated sequentially
        SequentialUpdate = 0,
        ///DAC with new data is updated, then DAC returns to sequence
        ImmediateUpdate,
        ///All DAC configured ports use the data in DACPRSTDAT1
        SameData1,
        ///All DAC configured ports use the data in DACPRSTDAT2
        SameData2   
    };
    
    ///Temperature sensors
    enum TempSensor_e
    {
        ///Internal Die Temp
        Internal = 0,
        ///Diode connected Q1
        External1,
        ///Diode connected Q2
        External2
    };
	
	static const uint8_t MAX_REGISTER_ADRS = 0x73;
    
    ///Command results
    enum CmdResult_e
    {
        ///Failed operation
        OpFailure = 0, 
        ///Successful operation
        Success 
    };
    
    MAX113XX_Pixi(Device_e device, PinName cnvt=NC);
    
    ///@brief Read single ended ADC configured port.\n
    ///Library supports single sweep, or continuous sweep ADC modes only
    ///@param[in] port - single ended ADC configured port
    ///@param[out] data - contents of ADC data register
    ///@return Result of operation
    CmdResult_e singleEndedADCRead(Ports_e port, uint16_t &data);
    
    ///@brief Read differential ADC configured port\n
    ///Library supports single sweep, or continuous sweep ADC modes only
    ///@param[in] posPort - positive port
    ///@param[out] data - contents of positive port ADC data register
    ///@return Result of operation
    CmdResult_e differentialADCRead(Ports_e posPort, int16_t &data);
    
    ///@brief Write DAC configured port
    ///@param[in] port - DAC configured port
    ///@param[in] data - value to be written to DAC data register
    ///@return Result of operation
    CmdResult_e dacWrite(Ports_e port, const uint16_t data);
    
    ///@brief Write DAC configured port and read ADC for port\n
    ///Library supports single sweep, or continuous sweep ADC modes only
    ///@param[in] port - DAC w/ADC Monitor configured port
    ///@param[in] data - value to be written to DAC data register
    ///@param[out] adcData - value read from adc
    ///@return Result of operation
    CmdResult_e dacWriteADCMonitor(Ports_e port, const uint16_t data, 
                                   uint16_t &adcData);
    
    ///@brief Reads gpi configured port
    ///@param[in] port - gpi congigured port to be read
    ///@param[out] state - lsb of state matches port state
    ///@return Result of operation 
    CmdResult_e gpioRead(Ports_e port, uint8_t &state);
    
    ///@brief Writes gpo configured port with lsb of state
    ///@param[in] port - gpo congigured port to be written
    ///@param[in] state - lsb of state is written to port
    ///@return Result of operation 
    CmdResult_e gpioWrite(Ports_e port, const uint8_t state);
    
    ///@brief Sets the state of a software controlled analog switch
    ///@param[in] lowPort - Port with lowest index
    ///@param[in] state - True for closed, false for hi-z
    ///@return Result of operation 
    CmdResult_e setAnalogSwitchState(Ports_e lowPort, bool state);
    
    ///@brief Reads temperature sensor
    ///@param[in] sensor - internal, or external sensor one or two
    ///@return Result of operation
    CmdResult_e readTempSensor(TempSensor_e sensor, float &data);
    
    ///@brief Dumps pixi memory to provided Serial object
    ///@param[in] ser - output device
    ///@return None
    void dumpMemory(Serial &ser);

protected:
    
    Device_e m_device;
    DigitalOut m_cnvt;
    
    ///@brief Writes given register with data
    ///@param[in] reg - register to be written
    ///@param[in] data - data to write
    ///@return none
    virtual void writeRegister(uint8_t reg, const uint16_t data) = 0;
    
    ///@brief Reads given register
    ///@param[in] reg - register to read
    ///@return contents of register
    virtual uint16_t readRegister(uint8_t reg) = 0;
    
    ///@brief Writes a block of data starting at given register
    ///@param[in] reg - register to start writing at
    ///@param[in] data - pointer to data buffer
    ///@param[in] num_reg - number of registers to be written
    ///@return none
    virtual void blockWrite(uint8_t reg, const uint16_t *data, 
                            const uint8_t num_reg) = 0;
    
    ///@brief Reads a block of data starting at given register
    ///@param[in] reg - register to start reading at
    ///@param[in] data - pointer to data buffer
    ///@param[in] num_reg - number of registers to be read
    ///@return none
    virtual void blockRead(uint8_t reg, uint16_t *data, 
                           const uint8_t num_reg) = 0;
};


/**
@brief SPI Declaration for MAX113XX parts
*/
class MAX113XX_SPI: public MAX113XX_Pixi
{

public:

    ///@brief MAX113XX_SPI Constructor
    ///@param[in] spiBus - reference to SPI bus for this device
    ///@param[in] cs - pin to be used for chip select
    ///@param[in] device - pixi device; MAX11300, MAX11301,...
    ///@param[in] cnvrt - pin to be used for convert
    MAX113XX_SPI(SPI & spiBus, PinName cs, MAX113XX_Pixi::Device_e device, 
                 PinName cnvt=NC);
    
    ///@brief MAX113XX_SPI Destructor
    ~MAX113XX_SPI();
    
private:

    SPI & m_spiBus;
    DigitalOut m_cs;
    
    virtual void writeRegister(uint8_t reg, const uint16_t data);
    
    virtual uint16_t readRegister(uint8_t reg);
    
    virtual void blockWrite(uint8_t reg, const uint16_t *data, 
                            const uint8_t num_reg);
    
    virtual void blockRead(uint8_t reg, uint16_t *data, const uint8_t num_reg);
};


/**
@brief I2C Declaration for MAX113XX parts
*/
class MAX113XX_I2C: public MAX113XX_Pixi
{

public:

    ///I2C Addresses
    static const uint8_t I2C_ADRS0 = 0x38;
    static const uint8_t I2C_ADRS1 = 0x39;
    static const uint8_t I2C_ADRS2 = 0x3A;
    static const uint8_t I2C_ADRS3 = 0x3B;
    static const uint8_t I2C_ADRS4 = 0x3C;
    static const uint8_t I2C_ADRS5 = 0x3D;
    static const uint8_t I2C_ADRS6 = 0x3E;
    static const uint8_t I2C_ADRS7 = 0x3F;
    
    ///@brief MAX113XX_I2C Constructor
    ///@param[in] i2cBus - reference to I2C bus for this device
    ///@param[in] device - pixi device; MAX11300, MAX11301,...
    ///@param[in] cnvrt - pin to be used for convert
    MAX113XX_I2C(I2C &i2cBus, MAX113XX_Pixi::Device_e device, uint8_t i2cAdrs, 
    PinName cnvt=NC);
    
    ///@brief MAX113XX_I2C Destructor
    ~MAX113XX_I2C();
    
private:

    I2C &m_i2cBus;
    uint8_t m_w_adrs, m_r_adrs;
    
    virtual void writeRegister(uint8_t reg, const uint16_t data);
    
    virtual uint16_t readRegister(uint8_t reg);
    
    virtual void blockWrite(uint8_t reg, const uint16_t *data, 
                            const uint8_t num_reg);
    
    virtual void blockRead(uint8_t reg, uint16_t *data, const uint8_t num_reg);
};


#endif /* _MAX113XX_PIXI_H_ */
