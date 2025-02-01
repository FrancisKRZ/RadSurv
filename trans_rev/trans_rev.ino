#include "axon.h"

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

// Radio Device, connects Chip Enable and Chip Select Not
RF24 radio(D9, D10);  // CE, CSN



unsigned char addr[] = "a1"; // Address as a byte array

unsigned short rand_clock(){
  return random(0, 9);
}

// Counts cycles no information has been received
unsigned long silent_counter = 0;

/* Micro Controller */
void setup() {

    Serial.begin(9600);

    // Packet address
    Packet.set_address(addr, 1, 2); // Set address with length 2 (including null terminator)

    // Set Power Amplifier (PA) level and Low Noise Amplifier (LNA) state
    radio.setPALevel(RF24_PA_MIN);

    // Default Status: OFF
    // OFF: 0   READING: 1    WRITING: 2
    unsigned short status = Packet.get_status();

    if (status == 2){
      radio.stopListening();
    }

    // Built-In LED
    pinMode(LED_BUILTIN, OUTPUT);
}

/*  
  Devices must have the following capabilities,
    By default, all devices are on OFF status, not reading or writing
    therefor after a short while (some cycles) a device must write and immediately read

    The time frame for writing after not hearing any signals must be asynchronous such as
    to avoid multiple devices doing the same sequence synchronously and having a radio deadlock.

    We do this if we want dedicated READ and WRITE devices to be assigned dynamically.

    Else we may have bi-directional communication by frequently altering status at random intervals.
*/
void loop() {

  // Radio online
  if (radio.available()){

    // Humbly turn on LED to indicate available status :^]
    digitalWrite(LED_BUILTIN, HIGH);

    String msg = "";

    radio.read();





    // Increase silent counter
    silent_counter = silent_counter + 1;
  }

  // LED OFF if Radio offline
  digitalWrite(LED_BUILTIN, LOW);
}



// eof