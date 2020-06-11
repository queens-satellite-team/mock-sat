#include <SPI.h>
#include "RF24.h"

RF24 transmitter(7, 8);
byte addresses[][6] = {"0"};

struct package {
  int id{1};
  char text[100] = "Text to transmit";
} Package;

Package data;

void setup() {
  Serial.begin(115200);
  delay(1000);
  transmitter.begin();
  transmitter.setChannel(115);
  transmitter.setPALevel(RF24_PA_MAX);
  transmitter.setDataRate(RF24_250KBPS);
  transmitter.openWritingPipe(addresses[0]);
  delay(1000);
}

void loop() {
  Serial.print("\nPackage:");
  Serial.print(data.id);
  Serial.print("\n");
  Serial.println(data.text);
  data.id++;
  delay(1000);
}
