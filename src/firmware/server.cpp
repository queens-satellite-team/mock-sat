#include <Arduino.h>
#include <Wire.h>

void setup() {
  Serial.begin(115200);
  Wire.begin();
}
void loop() {
  char inByte = ' ';
  if(Serial.available()){
    char inByte = Serial.read();
    Wire.beginTransmission(9);
    Wire.write(inByte);
    Wire.endTransmission();
  }
}
