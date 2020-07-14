#include <Arduino.h>
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
RF24 radio(7, 8); // CE, CSN
const byte address[6] = "00001";

void setup() {
  Serial.begin(115200);
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();
}
void loop() {
  if(Serial.available() > 32){
    char buffer[32] = "";
    int i = 0;
    while (i < 32) {
      buffer[i] = Serial.read();
      i++;
    }
    radio.write(&buffer, sizeof(buffer));
  }
}
