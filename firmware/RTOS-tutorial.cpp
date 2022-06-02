#include <Arduino_FreeRTOS.h>

// tasks
void Task_Print1(void *param);
void Task_Print2(void *param);

// task handelers
TaskHandle_t Task_Handle1;
TaskHandle_t Task_Handle2;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  // Parameters: task, name, stack memory, transferred parameters, priority, task handeler
  xTaskCreate(Task_Print1,"Task1",100,NULL,1,&Task_Handle1);
  xTaskCreate(Task_Print2,"Task2",100,NULL,2,&Task_Handle2);
}

void loop() {
  // Not needed when you are uding RTOS
}

void Task_Print1(void *param) {
  (void) param;
  while(1){
    Serial.println("Task1");
    vTaskDelay(1000/portTICK_PERIOD_MS);
  }
}

void Task_Print2(void *param) {
  (void) param;
  while(1){
    Serial.println("Task2");
    vTaskDelay(1000/portTICK_PERIOD_MS);
  }
}
