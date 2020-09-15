#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

#define CE_PIN 9
#define CSN_PIN 10
#define PACK_SIZE 13
#define BUF_SIZE 26

const byte numChars = 64;
char receivedChars[numChars];

boolean newData = false;

byte ledPin = 13; // the onboard LED

const byte slaveAddress[6] = {'RxAAA'}; //must be the same on the receiver

RF24 radio(CE_PIN, CSN_PIN); // Create a Radio

//===============

void setup()
{
    Serial.begin(115200);

    pinMode(ledPin, OUTPUT);
    digitalWrite(ledPin, HIGH);
    delay(200);
    digitalWrite(ledPin, LOW);
    delay(200);
    digitalWrite(ledPin, HIGH);

    radio.begin();
    radio.setDataRate(RF24_250KBPS);
    radio.setRetries(3, 5); // delay, count
    radio.openWritingPipe(slaveAddress);
    radio.stopListening();

    Serial.println("<Arduino is ready>");
}

//===============

void loop()
{
    recvWithStartEndMarkers();
    replyToPython();
    sendToReceiver();
}

//===============

void recvWithStartEndMarkers()
{
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

    while (Serial.available() > 0 && newData == false)
    {
        rc = Serial.read();

        if (recvInProgress == true)
        {
            if (rc != endMarker)
            {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars)
                {
                    ndx = numChars - 1;
                }
            }
            else
            {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker)
        {
            recvInProgress = true;
        }
    }
}

//===============

void replyToPython()
{
    if (newData == true)
    {
        Serial.print("<This just in ... ");
        Serial.print(receivedChars);
        Serial.print("   ");
        Serial.print(millis());
        Serial.print('>');
        // change the state of the LED everytime a reply is sent
        digitalWrite(ledPin, !digitalRead(ledPin));
        //newData = false;
    }
}

//===============

void sendToReceiver()
{
    if (newData == true)
    {
        bool rslt;

        rslt = radio.write(&receivedChars, sizeof(receivedChars));

        Serial.print("Data Sent ");
        Serial.print(receivedChars);
        if (rslt)
        {
            Serial.println("  Acknowledge received");
            newData = false;
        }
        else
        {
            Serial.println("  Tx failed");
        }
    }
}
