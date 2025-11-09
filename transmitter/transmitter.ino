/*
 * nRF24L01 Transmitter ---- Mega 2560
*/

// RTOS Library - Will be used for the sensor -> camera sequential circuits
#include <Arduino_FreeRTOS.h>
// Serial Communication Interface & Radio Comms nRF24L01 Libraries
#include <SPI.h>
#include "RF24.h"

// #define DEBUG_ENABLE


// Radio Pins
#define CE_PIN 7
#define CSN_PIN 8

// IR Movement Pin
#define IRM_PIN 12
bool pinStateCurrent  = LOW;
bool pinStatePrevious = LOW;
bool movement_logic();

// Radio Instantiation
RF24 radio(CE_PIN, CSN_PIN);
  // Define address/pipe to use.
const byte address[6] = "00001";

// RTOS Tasks
TaskHandle_t TaskTransmitter_Handler;

// Task Notification ISRs
void IRM_ISR_RISE();
void IRM_ISR_FALL();
void TaskTransmitter(void *pvParameters);

//===============================================================================
//  Initialization
//===============================================================================
void setup() {
  
  Serial.begin(9600);
  while (!Serial);

  // Radio setup
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_HIGH);
  radio.stopListening();

  pinMode(IRM_PIN, INPUT_PULLUP);

  // Attach interrupt
  attachInterrupt(digitalPinToInterrupt(IRM_PIN), IRM_ISR_RISE, RISING);
  attachInterrupt(digitalPinToInterrupt(IRM_PIN), IRM_ISR_FALL, FALLING);

  // Create the transmitter task
  xTaskCreate(TaskTransmitter, "Transmitter", 256, NULL, 2, &TaskTransmitter_Handler);

  // Start scheduler
  vTaskStartScheduler();
}


void IRM_ISR_RISE() {

  BaseType_t woken = pdFALSE;
  vTaskNotifyGiveFromISR(TaskTransmitter_Handler, &woken);
  if (woken) portYIELD_FROM_ISR();

}


void IRM_ISR_FALL() {

  BaseType_t woken = pdFALSE;
  vTaskNotifyGiveFromISR(TaskTransmitter_Handler, &woken);
  if (woken) portYIELD_FROM_ISR();

}


void TaskTransmitter(void *pvParameters) {

  for (;;) {
    ulTaskNotifyTake(pdTRUE, portMAX_DELAY);
    bool movement = digitalRead(IRM_PIN);
    radio.write(&movement, sizeof(bool));

    #ifdef DEBUG_ENABLE
    Serial.print("Motion status: ");
    Serial.println(movement);
    #endif
  }

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

    #ifdef DEBUG_ENABLE
      Serial.println(movement_detected);
    #endif
  }

  // Remove delays if using tasks
  delay(100);                          // Delay for 0.1 second, then repeat

}


bool movement_logic(){

  // Used to send additional zeroes to ensure readouts by the receiver(s)
  const static unsigned short ZERO_BUFFER = 16;

  pinStatePrevious = pinStateCurrent;      // Stores old state
  pinStateCurrent  = digitalRead(IRM_PIN); // Reads new state

  if (pinStatePrevious == LOW && pinStateCurrent == HIGH){
    return true;
  } else
  if (pinStatePrevious == HIGH && pinStateCurrent == LOW){

    bool send_false = false;

    for (int i = 0; i < ZERO_BUFFER; i++){
      radio.write(&send_false, sizeof(bool));
    }
    return false;
  } 

}


