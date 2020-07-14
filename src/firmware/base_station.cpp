#include <Wire.h>
// Include the required Wire library for I2C<br>#include <Wire.h>
int LED = 13;
void setup() {
    Serial.begin(115200);
    // Define the LED pin as Output
    pinMode (LED, OUTPUT);
    // Start the I2C Bus as Slave on address 9
    Wire.begin(9);
    // Attach a function to trigger when something is received.
    Wire.onReceive(receiveEvent);
}
void receiveEvent(int bytes) {
    char x = Wire.read();    // read one character from the I2C
    Serial.println(x);
}
void loop() {}
