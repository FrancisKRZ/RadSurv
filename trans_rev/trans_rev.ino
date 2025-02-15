// Radio System Management
#include "axon.h"
// Abstract List Implementation
#include "AList.h"


// CE: Chip Enable        -> D9
// CSN: Chip Select Not   -> D10
// IRQ: Interrupt         -> D6

// MISO: MiSo             -> D12
// MOSI: MoSi             -> D11
// SCK: Serial Clock      -> D13

#define CE    9
#define CSN   10
#define IRQ   6

#define MISO  12
#define MOSI  11
#define SCK   13

// Radio Device, connects Chip Enable and Chip Select Not
RF24 radio(CE, CSN);


/* Micro Controller */
void setup() {


}


void loop() {


}



// eof
