#include <Wire.h>
// Include the required Wire library for I2C<br>#include <Wire.h>
int LED = 13;
void setup() {
    Serial.begin(115200);
    pinMode (LED, OUTPUT);
    Wire.begin(9);
    Wire.onReceive(receiveEvent);
}
void receiveEvent(int bytes) {
    char x = Wire.read();
    Serial.print(x);
}
void loop() {}
