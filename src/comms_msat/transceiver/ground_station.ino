/************************************ HARDWARE CONFIG ******************************/
#define CMD1_pin 3
#define CMD2_pin 4
#define CMD3_pin 5
#define CE_pin 10
#define CSN_pin 9
/***********************************************************************************/
/******************************** INCLUDES AND GLOBALS *****************************/
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

byte addresses[][6] = {"TxAAA", "RxAAA"};
bool newData = false;
bool newCommand = false;
String OP_CODE;
const byte numChars = 32;
char receivedChars[numChars];
uint8_t chann = 81;
bool role = 1; // 1 = transmit, 0 = receive

struct commandStruct
{
  uint8_t _OP_CODE;
  char _data[];
} commandPack;

struct dataStruct
{
  uint64_t _packCount;
  String _receviedData;
} dataPack;

/***********************************************************************************/
/********************************** RADIO CONFIG ***********************************/
// Radio configuration
// 0 or 1 to distinguish between Tx = 0 and Rx = 1
bool radioNumber = 0;

// Hardware configuration:
RF24 radio(CE_pin, CSN_pin);
/***********************************************************************************/
/*************************************** setup() ***********************************/
void setup()
{
  //INITIALIZE PINS
  pinMode(CMD1_pin, OUTPUT);
  pinMode(CMD2_pin, OUTPUT);
  pinMode(CMD3_pin, OUTPUT);
  resetPins();

  // ESTABLISH RADIO PARAMETERS
  radio.begin();
  radio.setPALevel(RF24_PA_HIGH);
  radio.setAutoAck(true);
  radio.setChannel(chann); //0-125
  radio.setDataRate(RF24_250KBPS);
  radio.setRetries(3, 5); //delay, count
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

  //SETUP SERIAL CONNECTION WITH PYTHON SCRIPT
  Serial.begin(9600);
  Serial.flush();
  Serial.println("<Arduino is ready>");

  //RESET COMMAND FIELDS USED TO CONTROL RECEIVING / SENDING
  OP_CODE = '0';
  receivedChars[4] = '0'
}
/***********************************************************************************/
/************************************* loop () *************************************/
void loop()
{

  if (Serial.available()) // ground station control panel communicates to transeivers through serial connection
  {
    recvFromGS();               // received data held in receivedChars
    OP_CODE = receivedChars[4]; // update the OP_CODE

    if (OP_CODE.equals("1"))
    {
      commandOne();
    }
    else if (OP_CODE.equals("2"))
    {
      commandTwo();
    }
    else if (OP_CODE.equals("3"))
    {
      commandThree();
    }
  }
  delay(1000);
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
/********************************* resetPins() *************************************/
void resetPins()
{
  digitalWrite(CMD1_pin, HIGH);
  digitalWrite(CMD2_pin, HIGH);
  digitalWrite(CMD3_pin, HIGH);
  delay(250);
  digitalWrite(CMD1_pin, LOW);
  digitalWrite(CMD2_pin, LOW);
  digitalWrite(CMD3_pin, LOW);
  delay(250);
  digitalWrite(CMD1_pin, HIGH);
  digitalWrite(CMD2_pin, HIGH);
  digitalWrite(CMD3_pin, HIGH);
  delay(250);
  digitalWrite(CMD1_pin, LOW);
  digitalWrite(CMD2_pin, LOW);
  digitalWrite(CMD3_pin, LOW);
  delay(250);
  digitalWrite(CMD1_pin, HIGH);
  digitalWrite(CMD2_pin, HIGH);
  digitalWrite(CMD3_pin, HIGH);
  delay(250);
  digitalWrite(CMD1_pin, LOW);
  digitalWrite(CMD2_pin, LOW);
  digitalWrite(CMD3_pin, LOW);
}
/***********************************************************************************/
/********************************** commandOne *************************************/
void commandOne()
{
  // Stop listening so we may talk
  radio.stopListening();

  //update the OP_CODE to be sent
  commandPack._OP_CODE = 1;

  //update the data to be sent, last three numbers from the receivedChars
  //receivedChars is: cmd_1_###
  for (int i = 0; i < 3; i++)
  {
    commandPack._data[i] = receivedChars[i + 6];
  }

  //write to the satellite
  if (!radio.write(&commandPack, sizeof(commandPack)))
  {
    // if there is an unsuccesful write, let the user know
    Serial.println("<failed>");
  }
  else
  {
    // if there is a successful write, start receiving data
    Serial.println("<success>");
    newData = false;

    // start listening for responses
    radio.startListening();

    if (radio.available())
    {

      // while there is data ready
      while (radio.available())
      {

        // get the payload
        if (!radio.read(&dataPack, sizeof(dataPack)))
        {
          Serial.println("<failed>");
        }
        else
        {
          //send the payload data to ground station control panel
          Serial.print("<success");
          Serial.print(dataPack._packCount);
          Serial.print(dataPack._receivedData);
          Serial.println(">");
        }
      }
    }
  }
}
/***********************************************************************************/
/********************************** commandTwo *************************************/
void commandTwo()
{

  // Stop listening so we may talk
  radio.stopListening();

  //update the OP_CODE to be sent
  commandPack._OP_CODE = 1;

  //update the data to be sent, last three numbers from the receivedChars
  //receivedChars is: cmd_2_###
  for (int i = 0; i < 3; i++)
  {
    commandPack._data[i] = receivedChars[i + 6];
  }

  //write to the satellite
  if (!radio.write(&commandPack, sizeof(commandPack)))
  {
    // if there is an unsuccesful write, let the user know
    Serial.println("<failed>");
  }
  else
  {
    // if there is a successful write, start receiving data
    Serial.println("<success>");
    newData = false;

    // start listening for responses
    radio.startListening();

    if (radio.available())
    {

      // while there is data ready
      while (radio.available())
      {

        // get the payload
        if (!radio.read(&dataPack, sizeof(dataPack)))
        {
          Serial.println("<failed>");
        }
        else
        {
          //send the payload data to ground station control panel
          Serial.print("<success");
          Serial.print(dataPack._packCount);
          Serial.print(dataPack._receivedData);
          Serial.println(">");
        }
      }
    }
  }
}
/***********************************************************************************/
/********************************** commandThree ***********************************/
void commandThree()
{

  // Stop listening so we may talk
  radio.stopListening();

  //update the OP_CODE to be sent
  commandPack._OP_CODE = 3;

  //update the data to be sent, last three numbers from the receivedChars
  //receivedChars is: cmd_3_###
  for (int i = 0; i < 3; i++)
  {
    commandPack._data[i] = receivedChars[i + 6];
  }

  //write to the satellite
  if (!radio.write(&commandPack, sizeof(commandPack)))
  {
    // if there is an unsuccesful write, let the user know
    Serial.println("<failed>");
  }
  else
  {
    // if there is a successful write, start receiving data
    Serial.println("<success>");
    newData = false;

    // start listening for responses
    radio.startListening();

    if (radio.available())
    {

      // while there is data ready
      while (radio.available())
      {

        // get the payload
        if (!radio.read(&dataPack, sizeof(dataPack)))
        {
          Serial.println("<failed>");
        }
        else
        {
          //send the payload data to ground station control panel
          Serial.print("<success");
          Serial.print(dataPack._packCount);
          Serial.print(dataPack._receivedData);
          Serial.println(">");
        }
      }
    }
  }
}