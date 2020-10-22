/************************************ HARDWARE CONFIG ******************************/
#define CMD1_pin 3
#define CMD2_pin 4
#define CMD3_pin 5
#define CE_pin  9
#define CSN_pin 10
/***********************************************************************************/
/******************************** INCLUDES AND GLOBALS *****************************/
#include <SPI.h> 
#include <nRF24L01.h>
#include <RF24.h> 

byte addresses[][6] = {"TxAAA","RxAAA"};
bool newData = false;
bool newCommand = false; 
String command; 
const byte numChars = 32;
char receivedChars[numChars];
uint8_t chann = 81; 
bool role = 1; // 1 = transmit, 0 = receive 

struct dataStruct{
  char _tag;
  float _value; 
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
void setup() {
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
  radio.setDataRate( RF24_250KBPS );
  radio.setRetries(3,5); //delay, count
  if(radioNumber){
    radio.openWritingPipe(addresses[1]);
    radio.openReadingPipe(1,addresses[0]);
  }else{
    radio.openWritingPipe(addresses[0]);
    radio.openReadingPipe(1,addresses[1]);
  }
  radio.stopListening();

  //SETUP SERIAL CONNECTION WITH PYTHON SCRIPT 
  Serial.begin(9600);
  Serial.flush();
  Serial.println("<Arduino is ready>");
}
/***********************************************************************************/
/************************************* loop () *************************************/
void loop() {
  
  if ( Serial.available() )
  {
    command = '0';
    recvFromGS();  
    command = receivedChars[4];

    if ( command.equals("1") ){  
        commandOne();  
    } else if ( command.equals("2") ){
        commandTwo();   
    } else if ( command.equals("3") ){
        commandThree(); 
    }
    
  }
}
/***********************************************************************************/
/************************************* recvFromGS() ********************************/
void recvFromGS() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;
    
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }
        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}
/***********************************************************************************/
/********************************* resetPins() *************************************/
void resetPins(){
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
/********************************** changeMode**************************************/
void changeMode(){
  if (role == 1){
    role = 0;
    radio.startListening(); 
    //Serial.println("<changed to receving>");
  } else {
    role = 1; 
    radio.stopListening();
    //Serial.println("<changed to transmitting>");
  }
}
/***********************************************************************************/
/********************************** commandOne *************************************/
void commandOne(){
  dataPack._value = 1;
  dataPack._tag = "one";
  if (!radio.write( &dataPack, sizeof(dataPack) )){
    Serial.println("<failed>");
  } else {
    Serial.println("<success>");  
    newData = false;
  } 
}
/***********************************************************************************/
/********************************** commandTwo *************************************/
void commandTwo(){
  dataPack._value = 2;
  dataPack._tag = "two";
  if (!radio.write( &dataPack, sizeof(dataPack) )){
    Serial.println("<failed>");
  } else {
    Serial.println("<success>");
    newData = false;
  }

  //change to listening 

  // read incoming data

  // send to GS terminal 
  
}
/***********************************************************************************/
/********************************** commandThree ***********************************/
void commandThree(){
  dataPack._value = 3;
  dataPack._tag = "three";
  if (!radio.write( &dataPack, sizeof(dataPack) )){
    Serial.println("<failed>");
  } else {
    Serial.println("<success>");
    newData = false;
  } 
}
