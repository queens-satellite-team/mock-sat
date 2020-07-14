#include <Wire.h>
int x = 0;

void setup() {
  Wire.begin(9600);
}

void loop() {
  Wire.beginTransmission(4);
  Wire.write(x);
  Wire.endTransmission();
  x++;
  if (x > 5) x = 0;
  delay(500);
}
