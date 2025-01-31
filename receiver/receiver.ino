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


RF24 radio(D9, D10);  // CE, CSN

const byte rf_addr [][6] = {"00001", "00002"};
bool rf_active = 0;
unsigned long msg_sent = 0;
unsigned long msg_recv = 0;

struct DataPacket {
  String msg;
  unsigned long msg_count;
};

DataPacket Packet;


void setup(){

  Serial.begin(9600);
  
  pinMode(LED_BUILTIN, OUTPUT);

  radio.begin();
  radio.openReadingPipe(0, rf_addr[0]);
  radio.setPALevel(RF24_PA_MIN);

  radio.startListening();
}

void loop(){

  // Radio is active
  if (radio.available()){

    radio.read(&Packet, sizeof(DataPacket));

    digitalWrite(LED_BUILTIN, HIGH);
    Serial.print("MRECV");

    Serial.print(Packet.msg_count);
  }
  

  digitalWrite(LED_BUILTIN, LOW);
  delay(250);
}









