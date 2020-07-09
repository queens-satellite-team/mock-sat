#include <Arduino.h>
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
RF24 radio(7, 8);
const byte address[6] = "00001";
void setup() {
  Serial.begin(115200);
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MAX);
  radio.stopListening();
}

void loop() {
  if (Serial.available() > 32) {
    /*
    char byte[32];
    for (int i = 0; i < 32; ++i) {
        byte[i] = Serial.read();
    }
    */
    radio.write(&byte, sizeof(byte));
  } else {
    delay(100);
  }
}
