#include <Arduino_FreeRTOS.h>

// define two tasks for Blink & AnalogRead
void TaskBlink( void *pvParameters );
void TaskAnalogRead( void *pvParameters );

// the setup function runs once when you press reset or power the board
void setup() {

// initialize serial communication at 9600 bits per second:
Serial.begin(9600);

xTaskCreate(TaskBlink,"Blink",128,NULL,2,NULL);
xTaskCreate(TaskAnalogRead,"AnalogRead",128,NULL,1,NULL);

vTaskStartScheduler();

  // Now the task scheduler, which takes over control of scheduling individual tasks, is automatically started.
}

void loop()
{
  // Empty. Things are done in Tasks.
}

/*--------------------------------------------------*/
/*---------------------- Tasks ---------------------*/
/*--------------------------------------------------*/

void TaskBlink(void *pvParameters)  // This is a task.
{

  Serial.print("TASK BLINK\n");
  
  // initialize digital pin 13 as an output.
  pinMode(7, OUTPUT);

  while(1) // A Task shall never return or exit.
  {
    digitalWrite(7, HIGH);   // turn the LED on (HIGH is the voltage level)
    vTaskDelay( 1000 / portTICK_PERIOD_MS ); // wait for one second
    digitalWrite(7, LOW);    // turn the LED off by making the voltage LOW
    vTaskDelay( 1000 / portTICK_PERIOD_MS ); // wait for one second
  }
}

void TaskAnalogRead(void *pvParameters)  // This is a task.
{

  Serial.print("TASK READ\n");
  
  (void) pvParameters;

  while(1)
  {
    // read the input on analog pin 0:
    int sensorValue = analogRead(A0);
    // print out the value you read:
    Serial.println(sensorValue);
    vTaskDelay(1);  // one tick delay (15ms) in between reads for stability
  }
}
