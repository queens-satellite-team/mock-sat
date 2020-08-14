#include <Arduino_FreeRTOS.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

//initialize i2c comm with orient sensor
Adafruit_BNO055 bno = Adafruit_BNO055(55);

#define VEL_ADDR 0x60   
#define ACC_ADDR 0x61

// define all tasks
void P_CNTRL( void *pvParameters );
void ORIENT_READ( void *pvParameters );

// define all functions
void I2C_WRITE(int value, int ADDR){

  Wire.beginTransmission(ADDR);
  Wire.write(64);                     // cmd to update the DAC
  Wire.write(value >> 4);        // the 8 most significant bits...
  Wire.write((value & 15) << 4); // the 4 least significant bits...
  Wire.endTransmission();

}

// the setup function runs once
void setup() {

  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);

  //initialize i2c library
  Wire.begin();

  //settings for orient sensor
  bno.begin();
  bno.setExtCrystalUse(true);

  //get first orientation reading 
  sensors_event_t event; 
  bno.getEvent(&event);

  //initialize all tasks
  xTaskCreate(P_CNTRL,"P_CNTRL",128,NULL,1,NULL);
  xTaskCreate(ORIENT_READ,"ORIENT_READ",128,NULL,2,NULL);

  // Now the task scheduler takes control
  vTaskStartScheduler();
  
}

void loop()
{
  // EMPTY. Things are done in Tasks.
}

/*--------------------------------------------------*/
/*---------------------- Tasks ---------------------*/
/*--------------------------------------------------*/

void P_CNTRL(void *pvParameters){
  //for initial test this will simply blink leds on the DAC outputs

  while(1){ 

    Serial.print("CNTRL\n");

    I2C_WRITE(4000, VEL_ADDR);
    I2C_WRITE(0, ACC_ADDR);
    vTaskDelay( 1000 / portTICK_PERIOD_MS ); //pause for 1 sec (delay function doesn't work with RTOS)
    I2C_WRITE(0, VEL_ADDR);
    I2C_WRITE(4000, ACC_ADDR);
    vTaskDelay( 1000 / portTICK_PERIOD_MS );

  }

  vTaskDelay(1);  // one tick delay (15ms) in between reads for stability
  
}

void ORIENT_READ(void *pvParameters){
  
  while(1){

    Serial.print("ORIENT\n");
  
    sensors_event_t event; 
    bno.getEvent(&event);

    Serial.print("X: ");
    Serial.print(event.orientation.x, 4);
    Serial.print("\n\n");

    vTaskDelay(1);

  }
 
  vTaskDelay(1);  // one tick delay (15ms) in between reads for stability
  
}
