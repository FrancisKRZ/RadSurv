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

// IR MV SENSOR
#define D2 2



RF24 radio(D9, D10);  // CE, CSN

const byte rf_addr [][6] = {"00001", "00002"};

struct DataPacket {
  char msg[4] = "";
  unsigned long msg_count = 0;
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
  radio.setPALevel(RF24_PA_MAX);

  // Sets radio as transmitter
  radio.stopListening();

  // Built-In LED
  pinMode(LED_BUILTIN, OUTPUT);

  // IR MV Sensor
  pinMode(D2, INPUT);
  
}


void loop() {

  if (digitalRead(D2)){
    // unsigned long MAX RANGE: 4,294,967,295
    Packet.msg_count = Packet.msg_count + 1;

    strcat(Packet.msg, "MVD");
    digitalWrite(LED_BUILTIN, HIGH);

  } else {

    strcat(Packet.msg, "");
    digitalWrite(LED_BUILTIN, LOW);

  }

  radio.write(&Packet, sizeof(DataPacket));

  Serial.println(Packet.msg); Serial.print(Packet.msg_count);

  delay(250);
}


// eof