/*
 * \brief Transmit bytes from serial to NRF24 transceiver, transmit bytes from NRF24
 * transceiver to serial.
 *
 * Read bytes from serial and append them to a data buffer until:
 *  a) No more bytes are in the serial port (Serial.available() == 0)
 *  b) The number of bytes in the data buffer is equal to NRF24 max message
 *     length.
 * If b) send the data buffer to the NRF24 to transmit, and continue to read
 * from serial until a) or b) is triggered again.
 * If a) send the data buffer to the NRF24 to transmit. Then check the NRF24
 * receive buffer to see if any bytes have been received. If they have transmit
 * each byte over serial.
 *
 * This code can be used for both the transmitter and receiver Arduinos.
 */
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
