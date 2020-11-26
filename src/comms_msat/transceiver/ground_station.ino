/***********************************************************************************/
/******************************** INCLUDES AND GLOBALS *****************************/
#include <SPI.h>
#include <RF24.h>

byte addresses[][6] = {"1Node", "2Node"};

/* globals for loop() */
bool newCommand = false;
String command;

/* globals for recvFromGS() */
bool newData = false;
const byte numChars = 32;
char receivedChars[numChars];

/* global data structure - maximum of 32 bytes can be sent as a packet */
struct dataStruct
{
  /* TYPE        NAME                  USE           BYTE LOCATION    */
  char flag;             //(command / data)           [0]
  char op_code;          //(command number)           [1]
  uint8_t data_len;      //(length of data)           [2]
  uint8_t data_start;    //(character to start)       [3]
  char data[20];         //(actual data)           [4:23]
  unsigned long _micros; //(return trip time)     [24:27]
  uint8_t data_end;      //(character to end)        [28]
} dataPack;

/***********************************************************************************/
/********************************** USER CONFIG ***********************************/
// Radio configuration
// 0 or 1 to distinguish between GRS = 0 and SAT = 1
bool radioNumber = 0;  // sets writing and reading pipe addresses
bool role = 1;         // 1 = transmit, 0 = receive
uint8_t channel = 100; // frequency channel

// Hardware configuration
RF24 radio(8, 10); //CE, CSN
/***********************************************************************************/
/*************************************** setup() ***********************************/
void setup()
{
  configSerial();
  configDataPack();

  radio.begin();
  radio.setPALevel(RF24_PA_HIGH);
  radio.setAutoAck(true);
  radio.setDataRate(RF24_250KBPS); // RF24_1MBPS or RF24_250KBPS

  if (radioNumber)
  {
    radio.openWritingPipe(addresses[1]);
    radio.openReadingPipe(1, addresses[0]);
  }
  else
  {
    radio.openWritingPipe(addresses[0]);
    radio.openReadingPipe(1, addresses[1]);
  }
  radio.stopListening();
}
/***********************************************************************************/
/************************************* loop () *************************************/
void loop()
{
  if (Serial.available())
  {
    // receive the command from the ground station, updates the newData flag
    recvFromGS();

    // if we're done collecting the new data...
    if (newData)
    {

      radio.stopListening();

      if (!radio.write(&receivedChars, sizeof(receivedChars)))
      {
        Serial.println(F("<failed>"));
      }
      else
      {
        Serial.println(F("<success>"));
        newData = false;
      }
    }
  }
  delay(500);
}
/******************************* configRadio ************************************/
void configRadio()
{
  radio.begin();
  radio.setPALevel(RF24_PA_HIGH);
  radio.setAutoAck(true);
  radio.setDataRate(RF24_250KBPS); // RF24_1MBPS or RF24_250KBPS

  if (radioNumber)
  {
    radio.openWritingPipe(addresses[1]);
    radio.openReadingPipe(1, addresses[0]);
  }
  else
  {
    radio.openWritingPipe(addresses[0]);
    radio.openReadingPipe(1, addresses[1]);
  }
  radio.stopListening();
}
/***********************************************************************************/
/********************************* configSerial *********************************/
void configSerial()
{
  Serial.begin(9600);
  Serial.flush();
  Serial.println("<Arduino is ready>");
}
/***********************************************************************************/
/********************************** configDataPack ******************************/
void configDataPack()
{
  dataPack.flag = '0';
  dataPack.op_code = '0';
  dataPack.data_len = 0;
  dataPack.data_start = B10101010;
  dataPack.data_end = B01010101;
}
/***********************************************************************************/
/************************************* recvFromGS() ********************************/
void recvFromGS()
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
/***********************************************************************************/
/********************************** commandOne *************************************/
void commandOne()
{
  Serial.println("Command One Reached"); //debugging

  //debugging
  Serial.print("Updated Data: ");
  Serial.println(dataPack.data);
  Serial.print(" Flag: ");
  Serial.println(dataPack.flag);

  radio.stopListening();

  if (!radio.write(&dataPack, sizeof(dataPack)))
  {
    Serial.println(F("Failed to send Command One"));
  }
  else
  {
    Serial.println(F("Sent Command One"));
    newCommand = false;
  }
}
/***********************************************************************************/
/********************************** commandTwo *************************************/
void commandTwo()
{
  Serial.println("Command Two Reached"); //debugging

  // update the data to be sent
  dataPack.flag = 2;
  dataPack.data[0] = '2';

  //debugging
  Serial.print("Updated Data: ");
  Serial.print(" Flag: ");
  Serial.print(dataPack.flag);
  Serial.print(" Data: ");
  Serial.println(dataPack.data[0]);

  radio.stopListening();

  if (!radio.write(&dataPack, sizeof(dataPack)))
  {
    Serial.println(F("Failed to send Command Two"));
  }
  else
  {
    Serial.println(F("Sent Command Two"));
    newCommand = false;
  }
}
/***********************************************************************************/
/********************************** commandThree ***********************************/
void commandThree()
{
  Serial.println("Command Three Reached"); //debugging

  // update the data to be sent
  dataPack.flag = 3;
  dataPack.data[0] = '3';
  Serial.print("Updated Data: ");
  Serial.print(" Flag: ");
  Serial.print(dataPack.flag);
  Serial.print(" Data: ");
  Serial.println(dataPack.data[0]);

  radio.stopListening();

  if (!radio.write(&dataPack, sizeof(dataPack)))
  {
    Serial.println(F("Failed to send Command Three"));
  }
  else
  {
    Serial.println(F("Sent Command Three"));
    newCommand = false;
  }
} //end_commandThree
  /***********************************************************************************/