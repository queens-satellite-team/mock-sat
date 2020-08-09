List of tasks to run on Arduino FreeRTOS for moc-sat single axis system
-

1. ADCS read and control

    - read BNO055 (through I2C)
    - read Light Sensors
    - read Current Motor Data (read two analog)
    - set enable and direction (set two digital)
    - set desired vel (PWM for arduino or analog through I2C DAC)
    - set desired acc (analog through I2C DAC)
    
    
2. Focus and take photo

    - currently a raspi cam, will this work via arduino?
      - if not should we have a master raspi to take photos when the arduino returns okay?
      - would we be able to setup communication with the pi while using FreeRTOS?
    

3. Transmission of desired direction vector

    - is the transmitter controlled by SPI? 
    - this value should be given to ADCS function (then perhaps increase ADCS function priority?)
    

4. Transmission of photo information

    - likely the most intensive function/operation
    - can this be set as a 'background process' do be done in chunks? or should it be done all at once?
    
5. Emergency stop

    - simply a high priority function that can read a button or remote signal and stop all processes
    
