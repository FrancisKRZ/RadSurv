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

void setup() {

  Serial.begin(9600);

  radio.begin();
  
  // We'll utilize 00002 as our Writing Pipe
  radio.openWritingPipe(rf_addr[1]);
  // We'll utilize 00001 as our Reading Pipe
  // radio.openReadingPipe(1, rf_addr[0]);

  // ??
  radio.setPALevel(RF24_PA_MIN);

  // Sets radio as transmitter
  radio.stopListening();

  // Built-In LED
  pinMode(LED_BUILTIN, OUTPUT);
}


void loop() {


  msg_sent = msg_sent + 1;

  Packet.msg_count = msg_sent;
  Packet.msg = "";

  radio.write(&Packet, sizeof(DataPacket));

  Serial.print("MTRAN");                      
  Serial.print(Packet.msg);

  digitalWrite(LED_BUILTIN, LOW);

  delay(500);

  digitalWrite(LED_BUILTIN, HIGH);

}


