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


#include "MAX113XX_Pixi.h"


//20 port devices
#if defined(_MAX11300_DESIGNVALUE_H_) || defined(_MAX11301_DESIGNVALUE_H_) 

static const uint16_t configDesignVals[18] = {
    gpo_data_15_to_0_DESIGNVALUE,
    gpo_data_19_to_16_DESIGNVALUE,
    0, //reserved
    device_control_DESIGNVALUE,
    interrupt_mask_DESIGNVALUE,
    gpi_irqmode_7_to_0_DESIGNVALUE,
    gpi_irqmode_15_to_8_DESIGNVALUE,
    gpi_irqmode_19_to_16_DESIGNVALUE,
    0, //reserved
    dac_preset_data_1_DESIGNVALUE,
    dac_preset_data_2_DESIGNVALUE,
    tmp_mon_cfg_DESIGNVALUE,
    tmp_mon_int_hi_thresh_DESIGNVALUE,
    tmp_mon_int_lo_thresh_DESIGNVALUE,
    tmp_mon_ext1_hi_thresh_DESIGNVALUE,
    tmp_mon_ext1_lo_thresh_DESIGNVALUE,
    tmp_mon_ext2_hi_thresh_DESIGNVALUE,
    tmp_mon_ext2_lo_thresh_DESIGNVALUE};
    
static const uint16_t portConfigDesignVals[20] = {
    port_cfg_00_DESIGNVALUE,
    port_cfg_01_DESIGNVALUE,
    port_cfg_02_DESIGNVALUE,
    port_cfg_03_DESIGNVALUE,
    port_cfg_04_DESIGNVALUE,
    port_cfg_05_DESIGNVALUE,
    port_cfg_06_DESIGNVALUE,
    port_cfg_07_DESIGNVALUE,
    port_cfg_08_DESIGNVALUE,
    port_cfg_09_DESIGNVALUE,
    port_cfg_10_DESIGNVALUE,
    port_cfg_11_DESIGNVALUE,
    port_cfg_12_DESIGNVALUE,
    port_cfg_13_DESIGNVALUE,
    port_cfg_14_DESIGNVALUE,
    port_cfg_15_DESIGNVALUE,
    port_cfg_16_DESIGNVALUE,
    port_cfg_17_DESIGNVALUE,
    port_cfg_18_DESIGNVALUE,
    port_cfg_19_DESIGNVALUE};

static const uint16_t dacDesignVals[20]= {
    dac_data_port_00_DESIGNVALUE,
    dac_data_port_01_DESIGNVALUE,
    dac_data_port_02_DESIGNVALUE,
    dac_data_port_03_DESIGNVALUE,
    dac_data_port_04_DESIGNVALUE,
    dac_data_port_05_DESIGNVALUE,
    dac_data_port_06_DESIGNVALUE,
    dac_data_port_07_DESIGNVALUE,
    dac_data_port_08_DESIGNVALUE,
    dac_data_port_09_DESIGNVALUE,
    dac_data_port_10_DESIGNVALUE,
    dac_data_port_11_DESIGNVALUE,
    dac_data_port_12_DESIGNVALUE,
    dac_data_port_13_DESIGNVALUE,
    dac_data_port_14_DESIGNVALUE,
    dac_data_port_15_DESIGNVALUE,
    dac_data_port_16_DESIGNVALUE,
    dac_data_port_17_DESIGNVALUE,
    dac_data_port_18_DESIGNVALUE,
    dac_data_port_19_DESIGNVALUE};
      
#endif

//12 port devices...
#if defined(_MAX11311_DESIGNVALUE_H_) || defined(_MAX11312_DESIGNVALUE_H_)
static const uint16_t portConfigDesignVals[12] = {
    port_cfg_p0_DESIGNVALUE,
    port_cfg_p1_DESIGNVALUE,
    port_cfg_p2_DESIGNVALUE,
    port_cfg_p3_DESIGNVALUE,
    port_cfg_p4_DESIGNVALUE,
    port_cfg_p5_DESIGNVALUE,
    port_cfg_p6_DESIGNVALUE,
    port_cfg_p7_DESIGNVALUE,
    port_cfg_p8_DESIGNVALUE,
    port_cfg_p9_DESIGNVALUE,
    port_cfg_p10_DESIGNVALUE,
    port_cfg_p11_DESIGNVALUE};
#endif
    
    
//************************** Base Class member fxs *****************************
MAX113XX_Pixi::MAX113XX_Pixi(Device_e device, PinName cnvt):
m_device(device), m_cnvt(cnvt, 1)
{
}

//*********************************************************************
MAX113XX_Pixi::CmdResult_e MAX113XX_Pixi::singleEndedADCRead(Ports_e port, 
                                                             uint16_t &data)
{
    MAX113XX_Pixi::CmdResult_e result = MAX113XX_Pixi::OpFailure;
    
    //check for type of device
    if(m_device == MAX11300 || m_device == MAX11301) //20 port device
    {
        //is this port configured for this operation?
        if(((portConfigDesignVals[port] & 0xF000) >> 12) == MAX113XX_Pixi::MODE_7)
        {
            //Is device configured for continuous sweep?
            if((device_control_DESIGNVALUE & device_control_ADCCTL) != MAX113XX_Pixi::ContinuousSweep)
            {
                //No, generate sample requests for averaging
                uint8_t num_samples = ((portConfigDesignVals[port] & port_cfg_00_funcprm_nsamples) >> 5);
                num_samples = (1 << num_samples);
                
                while(num_samples--)
                {
                    m_cnvt = 0;
                    wait_us(1);
                    m_cnvt = 1;
                    wait_us(100);
                }
            }
            
            data = readRegister((adc_data_port_00 + port));
            
            result = MAX113XX_Pixi::Success;
        }
    }
    else //12 port device
    {
    }
    
    return result;
}

//*********************************************************************
MAX113XX_Pixi::CmdResult_e MAX113XX_Pixi::differentialADCRead(Ports_e posPort, 
                                                              int16_t &data)
{
    MAX113XX_Pixi::CmdResult_e result = MAX113XX_Pixi::OpFailure;
    
    //check for type of device
    if(m_device == MAX11300 || m_device == MAX11301) //20 port device
    {
        //is this port configured for this operation?
        if(((portConfigDesignVals[posPort] & 0xF000) >> 12) == MAX113XX_Pixi::MODE_8)
        {
            //Is device configured for continuous sweep?
            if((device_control_DESIGNVALUE & device_control_ADCCTL) != MAX113XX_Pixi::ContinuousSweep)
            {
                //No, generate sample requests for averaging
                uint8_t num_samples = ((portConfigDesignVals[posPort] & port_cfg_00_funcprm_nsamples) >> 5);
                num_samples = (1 << num_samples);
                
                while(num_samples--)
                {
                    m_cnvt = 0;
                    wait_us(1);
                    m_cnvt = 1;
                    wait_us(100);
                }
            }
            
            data = readRegister((adc_data_port_00 + posPort));
            if(data & 0x0800)
            {
                data |= 0xF000;
            }
            
            result = MAX113XX_Pixi::Success;
        }
    }
    else //12 port device
    {
    }
    
    return result;
}

//*********************************************************************
MAX113XX_Pixi::CmdResult_e MAX113XX_Pixi::dacWrite(Ports_e port, 
                                                       const uint16_t data)
{
    MAX113XX_Pixi::CmdResult_e result = MAX113XX_Pixi::OpFailure;
    
    if(m_device == MAX11300 || m_device == MAX11301) //20 port device
    {
        if(((portConfigDesignVals[port] & 0xF000) >> 12) == MAX113XX_Pixi::MODE_5)
        {
            writeRegister((dac_data_port_00 + port) , data);
            result = MAX113XX_Pixi::Success;
        }
    }
    else //12 port device
    {
    }
    
    return result;
}

//*********************************************************************
MAX113XX_Pixi::CmdResult_e MAX113XX_Pixi::dacWriteADCMonitor(Ports_e port, 
                                                            const uint16_t data, 
                                                            uint16_t &adcData)
{
    MAX113XX_Pixi::CmdResult_e result = MAX113XX_Pixi::OpFailure;
    
    if(m_device == MAX11300 || m_device == MAX11301) //20 port device
    {
        if(((portConfigDesignVals[port] & 0xF000) >> 12) == MAX113XX_Pixi::MODE_6)
        {
            writeRegister((dac_data_port_00 + port) , data);
            
            m_cnvt = 0;
            wait_us(1);
            m_cnvt = 1;
            wait_us(100);

            adcData = readRegister((adc_data_port_00 + port));
            
            result = MAX113XX_Pixi::Success;
        }
    }
    else //12 port device
    {
    }
    
    return result;
}

//*********************************************************************
MAX113XX_Pixi::CmdResult_e MAX113XX_Pixi::gpioRead(Ports_e port, uint8_t &state)
{
    MAX113XX_Pixi::CmdResult_e result = MAX113XX_Pixi::OpFailure;
    
    if(m_device == MAX11300 || m_device == MAX11301) //20 port device
    {
        if(((portConfigDesignVals[port] & 0xF000) >> 12) == MAX113XX_Pixi::MODE_1)
        {
            if(port < MAX113XX_Pixi::PORT16)
            {
                state = (readRegister(gpi_data_15_to_0) >> port);
            }
            else
            {
                state = (readRegister(gpi_data_19_to_16) >> (port - MAX113XX_Pixi::PORT16));
            }
            
            result = MAX113XX_Pixi::Success;
        }
    }
    else //12 port device
    {
    }
    
    return result;
}

//*********************************************************************
MAX113XX_Pixi::CmdResult_e MAX113XX_Pixi::gpioWrite(Ports_e port, 
                                                    const uint8_t state)
{
    uint16_t temp;
    uint16_t port_mask;
    
    MAX113XX_Pixi::CmdResult_e result = MAX113XX_Pixi::OpFailure;
    
    if(m_device == MAX11300 || m_device == MAX11301) //20 port device
    {
        if(((portConfigDesignVals[port] & 0xF000) >> 12) == MAX113XX_Pixi::MODE_3)
        {
            if(port < MAX113XX_Pixi::PORT16)
            {
                port_mask = (1 << port);
                temp = readRegister(gpo_data_15_to_0);
                if(state & 0x01)
                {
                    temp |= port_mask;
                }
                else
                {
                    temp &= ~port_mask;
                }
                writeRegister(gpo_data_15_to_0, temp);
            }
            else
            {
                port_mask = (1 << (port - MAX113XX_Pixi::PORT16));
                temp = readRegister(gpo_data_19_to_16);
                if(state & 0x01)
                {
                    temp |= port_mask;
                }
                else
                {
                    temp &= ~port_mask;
                }
                writeRegister(gpo_data_19_to_16, temp);
            }
            
            result = MAX113XX_Pixi::Success;
        }
    }
    else //12 port device
    {
    }
    
    return result;
}

//*********************************************************************
MAX113XX_Pixi::CmdResult_e MAX113XX_Pixi::setAnalogSwitchState(Ports_e lowPort, 
                                                               bool state)
{
    MAX113XX_Pixi::CmdResult_e result = MAX113XX_Pixi::OpFailure;
    
    if(m_device == MAX11300 || m_device == MAX11301) //20 port device
    {
        if(((portConfigDesignVals[lowPort] & 0xF000) >> 12) == MAX113XX_Pixi::MODE_12)
        {
            uint16_t data = readRegister(port_cfg_00 + lowPort);
            if(state)
            {
                data = ((data & 0x0FFF) | (MAX113XX_Pixi::MODE_12 << 12));
            }
            else
            {
                data = ((data & 0x0FFF) | (MAX113XX_Pixi::MODE_0 << 12));
            }
            writeRegister((port_cfg_00 + lowPort), data);
            
            result = MAX113XX_Pixi::Success;
        }
    }
    else //12 port device
    {
    }
    
    return result;
}

//*********************************************************************
MAX113XX_Pixi::CmdResult_e MAX113XX_Pixi::readTempSensor(TempSensor_e sensor, 
                                                         float &data)
{
    MAX113XX_Pixi::CmdResult_e result = MAX113XX_Pixi::OpFailure;
    int16_t temp = 0;
    
    if(m_device == MAX11300 || m_device == MAX11301) //20 port device
    {
        switch(sensor)
        {
            case Internal:
                if(device_control_DESIGNVALUE & device_control_TMPCTLINT)
                {
                    temp = readRegister(tmp_int_data);
                    result = MAX113XX_Pixi::Success;
                }
            break;
            
            case External1:
                if(device_control_DESIGNVALUE & device_control_TMPCTLEXT0)
                {
                    temp = readRegister(tmp_ext1_data);
                    result = MAX113XX_Pixi::Success;
                }
            break;
            
            case External2:
                if(device_control_DESIGNVALUE & device_control_TMPCTLEXT1)
                {
                    temp = readRegister(tmp_ext2_data);
                    result = MAX113XX_Pixi::Success;
                }
            break;
        };
        
        if(result == MAX113XX_Pixi::Success)
        {
            if(temp & 0x0800)
            {
                temp |= 0xF000;
            }
            data = (temp/8.0F);
        }
    }
    else //12 port device
    {
    }
    
    return result;
}

//*********************************************************************
void MAX113XX_Pixi::dumpMemory(Serial &ser)
{
    uint16_t mem[0x74];
    
    blockRead(dev_id, mem, 0x74);
    for(uint8_t idx = 0; idx < 0x74; idx++)
    {
        ser.printf("Register 0x%02x = 0x%04x\r\n", idx, mem[idx]);
    }
    ser.printf("\r\n");
}


/// SPI first byte when writing MAX11300/11 
//(7-bit address in bits 0x7E; LSB=0 for write)
#define MAX113XXAddr_SPI_Write(RegAddr) ( (RegAddr << 1)     )

/// SPI first byte when reading MAX11300/11 
//(7-bit address in bits 0x7E; LSB=1 for read)
#define MAX113XXAddr_SPI_Read(RegAddr)  ( (RegAddr << 1) | 1 )

//*************************** SPI Implementation ******************************
MAX113XX_SPI::MAX113XX_SPI(SPI & spiBus, PinName cs, 
MAX113XX_Pixi::Device_e device, PinName cnvt):
MAX113XX_Pixi(device, cnvt), m_spiBus(spiBus), m_cs(cs, 1)
{
    if((m_device == MAX11300) || (m_device == MAX11301)) //20 port device
    {
        blockWrite(gpo_data_15_to_0, configDesignVals, 18);
        blockWrite(port_cfg_00, portConfigDesignVals, 20);
        blockWrite(dac_data_port_00, dacDesignVals, 20);
        wait(0.1);
    }
    else //12 port device
    {
    }
}

//*********************************************************************
MAX113XX_SPI::~MAX113XX_SPI()
{
    //empty block
}

//*********************************************************************
void MAX113XX_SPI::writeRegister(uint8_t reg, const uint16_t data)
{
    m_cs = 0;
    m_spiBus.write(MAX113XXAddr_SPI_Write(reg));
    m_spiBus.write(((0xFF00 & data) >> 8));
    m_spiBus.write((0x00FF & data));
    m_cs = 1;
}

//*********************************************************************    
uint16_t MAX113XX_SPI::readRegister(uint8_t reg)
{
    uint16_t rtn_val = 0;
    
    m_cs = 0;
    m_spiBus.write(MAX113XXAddr_SPI_Read(reg));
    rtn_val |= (m_spiBus.write(0xFF) << 8);
    rtn_val |= m_spiBus.write(0xFF);
    m_cs = 1;
    
    return rtn_val;
}

//*********************************************************************    
void MAX113XX_SPI::blockWrite(uint8_t reg, const uint16_t *data, 
                              const uint8_t num_reg)
{
    m_cs = 0;
    m_spiBus.write(MAX113XXAddr_SPI_Write(reg));
    for(uint8_t idx = 0; idx < num_reg; idx++)
    {
        m_spiBus.write(((0xFF00 & data[idx]) >> 8));
        m_spiBus.write((0x00FF & data[idx]));
    }
    m_cs = 1;
}

//*********************************************************************        
void MAX113XX_SPI::blockRead(uint8_t reg, uint16_t *data, const uint8_t num_reg)
{
    uint16_t temp;
    m_cs = 0;
    m_spiBus.write(MAX113XXAddr_SPI_Read(reg));
    for(uint8_t idx = 0; idx < num_reg; idx ++)
    {
        temp = 0;
        temp |= (m_spiBus.write(0xFF) << 8);
        temp |= m_spiBus.write(0xFF);
        data[idx] = temp;
    }
    m_cs = 1;
}


//*************************** I2C Implementation ******************************
MAX113XX_I2C::MAX113XX_I2C(I2C &i2cBus, MAX113XX_Pixi::Device_e device, 
uint8_t i2cAdrs, PinName cnvt):
MAX113XX_Pixi(device, cnvt), m_i2cBus(i2cBus), m_w_adrs(i2cAdrs << 1), 
m_r_adrs((i2cAdrs << 1) | 1)
{
    if((m_device == MAX11300) || (m_device == MAX11301)) //20 port device
    {
        blockWrite(gpo_data_15_to_0, configDesignVals, 18);
        blockWrite(port_cfg_00, portConfigDesignVals, 20);
        blockWrite(dac_data_port_00, dacDesignVals, 20);
        wait(0.1);
    }
    else //12 port device
    {
    }
}

//*********************************************************************
MAX113XX_I2C::~MAX113XX_I2C()
{
    //empty block
}

//*********************************************************************
void MAX113XX_I2C::writeRegister(uint8_t reg, const uint16_t data)
{
   char localData[3];
   uint8_t idx = 0;
   
   localData[idx++] = reg;
   localData[idx++] = ((data & 0xFF00) >> 8);
   localData[idx++] = (data & 0x00FF);
   
   m_i2cBus.write(m_w_adrs, localData, idx);
}

//*********************************************************************    
uint16_t MAX113XX_I2C::readRegister(uint8_t reg)
{
    uint16_t rtn_val = 0;
    
    char localData[2];
    localData[0] = reg;
    
    if(m_i2cBus.write(m_w_adrs, localData, 1, true) == 0)
    {
        if(m_i2cBus.read(m_r_adrs, localData, 2) == 0)
        {
            rtn_val |= (localData[0] << 8);
            rtn_val |= localData[1];
        }
    }
    
    return rtn_val;
}

//*********************************************************************    
void MAX113XX_I2C::blockWrite(uint8_t reg, const uint16_t *data, 
                               const uint8_t num_reg)
{
   uint16_t numBytes = ((num_reg * 2) + 1);
   //No variable length array
   char localData[MAX113XX_Pixi::MAX_REGISTER_ADRS];
   uint8_t idx(0), dataIdx(0);
   
   localData[idx++] = reg;
   do
   {
       localData[idx++] = ((data[dataIdx] & 0xFF00) >> 8);
       localData[idx++] = (data[dataIdx++] & 0x00FF);
   }
   while(idx < numBytes);
   
   m_i2cBus.write(m_w_adrs, localData, numBytes);  
}

//*********************************************************************        
void MAX113XX_I2C::blockRead(uint8_t reg, uint16_t *data, const uint8_t num_reg)
{
    uint16_t numBytes = (num_reg * 2);
	//No variable length array
	char localData[MAX113XX_Pixi::MAX_REGISTER_ADRS];
    localData[0] = reg;
    
    if(m_i2cBus.write(m_w_adrs, localData, 1, true) == 0)
    {
        if(m_i2cBus.read(m_r_adrs, localData, numBytes) == 0)
        {
            uint8_t dataIdx = 0;
            for(uint8_t idx = 0; idx < numBytes; idx += 2)
            {
                data[dataIdx] = 0;
                data[dataIdx] |= (localData[idx] << 8);
                data[dataIdx++] |= localData[idx + 1];
            }
        }
    }
}
