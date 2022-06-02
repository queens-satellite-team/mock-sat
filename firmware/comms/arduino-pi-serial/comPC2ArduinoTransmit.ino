#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
RF24 radio (9,10); // CE, CSN
const byte address[6] = "00001";
void setup() {
  Serial.begin(9600);
  Serial.print("Sent from transmitter");

  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();

  const char text[] = "It's working";
  radio.write(&text, sizeof(text));

}
void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    Serial.print("You sent me: ");
    Serial.println(data);

    //convert string to char array
    int dataLen = data.length()+1;
    char dataChar[dataLen];
    data.toCharArray(dataChar,dataLen);
    radio.write(&dataChar, sizeof(dataChar));
  }
}
