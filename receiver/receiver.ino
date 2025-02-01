#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

// CE: Chip Enable        -> D9
// CSN: Chip Select Not   -> D10
// IRQ: Interrupt         -> D6

// MISO: MiSo             -> D12
// MOSI: MoSi             -> D11
// SCK: Serial Clock      -> D13

#define D9    9
#define D10   10
#define IRQ   6

#define MISO  12
#define MOSI  11
#define SCK   13

#define D3 3


RF24 radio(D9, D10);  // CE, CSN

const byte rf_addr [][6] = {"00001", "00002"};

struct DataPacket {
  char msg[4] = "";
  unsigned long msg_count = 0;
};

DataPacket Packet;


void setup(){

  Serial.begin(9600);
  
  pinMode(LED_BUILTIN, OUTPUT);

  radio.begin();
  radio.openReadingPipe(0, rf_addr[1]);
  radio.setPALevel(RF24_PA_MAX);

  radio.startListening();

  pinMode(D3, OUTPUT);
}

void loop(){

  // Radio is active
  if (radio.available()){

    radio.read(&Packet, sizeof(DataPacket));

    Serial.println(Packet.msg); Serial.print(Packet.msg);

  }
  

  digitalWrite(LED_BUILTIN, LOW);
  delay(250);
}









