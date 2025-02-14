/*
 * nRF24L01 Transmitter ---- Mega 2560
 */
#include <SPI.h>
#include "RF24.h"

// Radio Pins
#define CE_PIN 7
#define CSN_PIN 8

// IR Movement Pin
#define IRM_PIN 12
bool pinStateCurrent  = LOW;
bool pinStatePrevious = LOW;
bool movement_logic();


RF24 radio(CE_PIN, CSN_PIN); // CE, CSN      // Define instance of RF24 object called 'radio' and define pins used

const byte address[6] = "00001";  // Define address/pipe to use.


//===============================================================================
//  Initialization
//===============================================================================
void setup() {

  // Serial.begin(9600);

  // while (!Serial){ };

  radio.begin();                  // Start instance of the radio object
  radio.openWritingPipe(address); // Setup pipe to write data to the address that was defined
  radio.setPALevel(RF24_PA_MAX);  // Set the Power Amplified level to MAX in this case
  radio.stopListening();          // We are going to be the transmitter, so we will stop listening

  // Read Movement
  pinMode(IRM_PIN, INPUT);

}
//===============================================================================
//  Main
//===============================================================================
void loop() {

  /* RTOS Opportunity , 
  Sequential circuit camera activation upon movement_detected
  for 3-5 minutes , then deactivation */


  bool movement_detected = movement_logic();

  while (movement_detected){

    radio.write(&movement_detected, sizeof(bool));
    movement_detected = movement_logic();
  }


  // if (digitalRead(IRM_PIN) == HIGH){
  //   Serial.println("HIGH");
  //   radio.write(&movement_detected, sizeof(bool));     // Write the char array.

  // }

  delay(500);                          // Delay for 1 second, then repeat

}


bool movement_logic(){

  pinStatePrevious = pinStateCurrent;      // Stores old state
  pinStateCurrent  = digitalRead(IRM_PIN); // Reads new state

  if (pinStatePrevious == LOW && pinStateCurrent == HIGH){
    return true;
  } else
  if (pinStatePrevious == HIGH && pinStateCurrent == LOW){
    return false;
  } 

}


