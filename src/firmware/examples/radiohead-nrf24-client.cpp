#include <Arduino.h>
#include <SPI.h>
#include <RadioHead.h>
#include <RadioHead/RHGenericSPI.h>
#include <RadioHead/RH_NRF24.h>

RH_NRF24 nrf24(8, 53);

void setup() {
  Serial.begin(9600);
  while (!Serial);
  if (!nrf24.init()) Serial.println("init failed");
  if (!nrf24.setChannel(1)) Serial.println("setChannel failed");
  if (!nrf24.setRF(RH_NRF24::DataRate2Mbps, RH_NRF24::TransmitPower0dBm))
    Serial.println("setRF failed");
}

void loop() {
  Serial.println("Sending to nrf24_server");
  uint8_t data[] = "Hello World!";
  nrf24.send(data, sizeof(data));

  nrf24.waitPacketSent();
  uint8_t buf[RH_NRF24_MAX_MESSAGE_LEN];
  uint8_t len = sizeof(buf);

  if (nrf24.waitAvailableTimeout(500)) {
    if (nrf24.recv(buf, &len)) {
      Serial.print("got reply: ");
      Serial.println((char *)buf);
    } else {
      Serial.println("recv failed");
    }
  } else {
    Serial.println("No reply, is nrf24_server running?");
  }
  delay(400);
}
