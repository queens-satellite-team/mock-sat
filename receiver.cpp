#include <SPI.h>
#include "RF24.h"

RF24 receiver(7, 8);
byte addresses[][6] = {"0"};

struct package {
  int id{1};
  char text[100] = "Received";
} Package;

Package data;

void setup() {
  Serial.begin(115200);
  delay(1000);
  receiver.begin();
  receiver.setChannel(115);
  receiver.setPALevel(RF24_PA_MAX);
  receiver.setDataRate(RF24_250KBPS);
  receiver.openReadingPipe(1, addresses[0]);
  receiver.startListening();
  delay(1000);
}

void loop() {
  if (receiver.available()) {
    while (receiver.available()) {
      receiver.read(&data, sizeof(data));
    }
    Serial.print("\nPackage:");
    Serial.print(data.id);
    Serial.print("\n");
    Serial.println(data.text);
  }
}
