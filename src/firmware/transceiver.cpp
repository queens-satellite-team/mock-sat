#include <Arduino.h>
#include <SPI.h>
#include <RadioHead.h>
#include <RadioHead/RHGenericSPI.h>
#include <RadioHead/RH_NRF24.h>

RH_NRF24 nrf24(8, 53);
uint8_t data[RH_NRF24_MAX_MESSAGE_LEN];
uint8_t read_byte = 1;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  if (!nrf24.init()) Serial.println("init failed");
  if (!nrf24.setChannel(1)) Serial.println("setChannel failed");
  if (!nrf24.setRF(RH_NRF24::DataRate2Mbps, RH_NRF24::TransmitPower0dBm))
    Serial.println("setRF failed!");
}

void loop() {
  int i = 0;
  while (Serial.available()) {
    if (i < RH_NRF24_MAX_MESSAGE_LEN) {
      data[i] = Serial.read();
      i++;
    } else {
      nrf24.send(data, sizeof(uint8_t)*i);
      nrf24.waitPacketSent();
      i = 0;
    }
  }
  if (i != 0) {
    nrf24.send(data, sizeof(data));
    nrf24.waitPacketSent();
  }
  while (nrf24.available()) {
    nrf24.recv(data, &read_byte);
    Serial.print(char(data[0]));
  }
}
