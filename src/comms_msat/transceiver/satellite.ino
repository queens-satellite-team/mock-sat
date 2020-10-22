/*********************** HARDWARE CONFIG ******************************/
#define CE_pin  7
#define CSN_pin 8
/***********************************************************************/

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
bool role = 0; 

struct dataStruct{
  char _tag;
  float _value; 
} dataPack;

/*********************** RADIO CONFIG ***********************************/
// Radio configuration
// 0 or 1 to distinguish between Tx = 0 and Rx = 1
bool radioNumber = 1; 

// Hardware configuration:
RF24 radio(CE_pin, CSN_pin);
/***********************************************************************/

void setup() {
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
  radio.startListening();

  //SETUP SERIAL CONNECTION WITH PYTHON SCRIPT 
  Serial.begin(9600);
  Serial.flush();
  Serial.println("<Arduino is ready>");
}

void loop() {
    radio.startListening();
    
    if( radio.available() ){                                             
      while ( radio.available() ) {                                   
        radio.read( &dataPack, sizeof(dataPack) );     
      }
      newData = true; 
    }

    if(newData == true){
      radio.stopListening();
      Serial.print(F("<Response: "));
      Serial.print(dataPack._value);
      Serial.println(F(">"));
      newData = false; 
    }

}
