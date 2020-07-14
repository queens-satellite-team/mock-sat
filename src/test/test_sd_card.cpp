#include <Arduino.h>
#include <SD.h>
#include <SPI.h>

const int CS_PIN = 53;
const String text = "This is sample text";

void setup() {
  char *file_name = "test.txt";
  Serial.begin(9600);

  Serial.println("Initializing SD card...");
  pinMode(CS_PIN, OUTPUT);
  if (SD.begin()) {
    Serial.println("SD card is ready to use");
  } else {
    Serial.println("SD card initialization failed");
    return;
  }
  delay(1000);
  File file = SD.open(file_name, FILE_WRITE);
  if (file) {
    Serial.println("File created successfully.");
    Serial.print("Writing to file: ");
    Serial.println(text);
    file.println(text.c_str());
    Serial.println("Closing file.");
    file.close();
    delay(1000);

    Serial.print("Reading From File: ");
    file = SD.open(file_name);
    String recieved = "";
    while (file.available()) {
      recieved += char(file.read());
    }
    Serial.print(recieved);
    Serial.println("Closing file");
    file.close();
    if (SD.remove(file_name)) {
      Serial.println("File deleted");
    } else {
      Serial.println("File not deleted");
    }
  } else {
    Serial.println("Error while creating file.");
  }
}

void loop() {
}
