/*
 * SimpleSerial - Rx (the slave or the receiver)
 * Checks the incoming data for duplicates. Havinig trouble with the same packet being sent
 * or not updating. Not sure which error it is becuase Arduino sucks for debugging. 
 */

#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

#define CE_PIN   9
#define CSN_PIN 10
#define PACK_SIZE 32

const byte thisSlaveAddress[6] = {'RxAAA'};

RF24 radio(CE_PIN, CSN_PIN);

char dataReceived[PACK_SIZE]; // this must match dataToSend in the TX
char dataPrev[PACK_SIZE];
char dataPack[PACK_SIZE];
bool newData = false;

//===========

void setup() 
{
    Serial.begin(115200);
    
    radio.begin();
    radio.setDataRate( RF24_250KBPS );
    radio.openReadingPipe(1, thisSlaveAddress);
    radio.startListening();

    Serial.println("Arduino is ready");
}

//=============

void loop() {
    getData();
    showData();
    delay(500); 
}

//==============

void getData() {
    if ( radio.available() ) {
        radio.read( &dataReceived, sizeof(dataReceived) );

        if(dataReceived == dataPrev)
        {
          newData = false;
          Serial.println("Error: Received the same packet.");
        } else {
          newData = true;
          memcpy(dataPack, dataReceived, sizeof(dataReceived));
          memcpy(dataPrev, dataReceived, sizeof(dataReceived));
          Serial.println("Success: Got a new packet."); 
        }
    }
}

void showData() {
    if (newData == true) {
        Serial.print("Data received ");
        Serial.println(dataPack);
        newData = false;
    }
}
