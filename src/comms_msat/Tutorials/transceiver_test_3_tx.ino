#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

#define CE_PIN 9
#define CSN_PIN 10
#define PACK_SIZE 13
#define BUF_SIZE 26

const byte numChars = 32;
char receivedChars[numChars];

boolean newData = false;

byte ledPin = 13; // the onboard LED

const byte slaveAddress[6] = {'RxAAA'}; //must be the same on the receiver

RF24 radio(CE_PIN, CSN_PIN); // Create a Radio

//===============

void setup()
{
    Serial.begin(115200);

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
    //receive the data packet from the python script
    recvWithStartEndMarkers();
    //relay that packet to the receiver
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

void replyToPython(bool rslt)
{
    if (rslt == true)
    {
        Serial.print("<Success: ");
        Serial.print(receivedChars);
        Serial.print(" sent to receiver.");
        Serial.print('>');
        newData = false;
    }
    else
    {
        Serial.print("<Error: Could not Transmit.>");
    }
}

//===============

void sendToReceiver()
{
    if (newData == true)
    {
        bool rslt;

        rslt = radio.write(&receivedChars, sizeof(receivedChars));
        // radio.write blocks until message is successfully acknowledged by the receiver or timeout/retransmit maxima are reached.

        replyToPython(rslt);
    }
}