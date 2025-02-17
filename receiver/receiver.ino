/*
 * nRF24L01 Receiver ---- Uno R3
*/

// RTOS Library - Utilized in handling alert system and radio communications by inter-tasks
#include <Arduino_FreeRTOS.h>
// Mutex support
#include <semphr.h>
// Serial Communication Interface & Radio Comms nRF24L01 Libraries
#include <SPI.h>
#include "RF24.h"

// DEBUG MODE ---- Prevents serial prints out from being compiled if not DEBUG_ENABLE not defined
// #define DEBUG_ENABLE

// nRF24
#define CE_PIN 7 
#define CSN_PIN 8

// [WIP] Alert Module
#define BUZZER_PIN 2

// Task Handles
TaskHandle_t TaskRFRecv_Handler;
TaskHandle_t TaskAlertMod_Handler;

// Task definitions
void TaskRFRecv(void *pvParameters);
void TaskAlertMod(void *pvParameters);

// Semaphore handler
SemaphoreHandle_t mutex;
// Global variable to be synchronized with mutex for RFRecv and AlertMod tasks
bool GLOBAL_ALERT = false;


// Radio Instantiation
RF24 radio(CE_PIN, CSN_PIN);
// Define address/pipe to use. This can be any 5 alphnumeric letters/numbers
const byte address[6] = "00001";


//===============================================================================
//  Initialization
//===============================================================================
void setup() {


  #ifdef DEBUG_ENABLE
  /*  Use Serial during Debugging only */
  Serial.begin(9600);
  // Wait for Serial init
  while (!Serial) { };
  #endif

  
  // Mutex creation
  mutex = xSemaphoreCreateMutex();

  #ifdef DEBUG_ENABLE
  if (mutex != NULL){
    Serial.println("Mutex Created");
  }
  #endif

  // Scoped Enumeration
  enum task_priorities {
                        LOW_PRIORITY   = 1,  // 1
                        MEDIUM_PRIORITY,     // 2
                        HIGH_PRIORITY        // 3
  };

  // Scoped Enum Priorities; LOW , MEDIUM , HIGH  {1, 2 ,3}
  task_priorities priorities;

  // Create a Standard Stack Size of 128 bits (16 bytes)
  const static uint32_t stackSize = 128;

  // Radio Comms Task   ----- 17 bytes
  xTaskCreate(TaskRFRecv, "RadioRecv", stackSize * 2, NULL, HIGH_PRIORITY, &TaskRFRecv_Handler);

  // Alert Module Task  ----- 16 bytes
  xTaskCreate(TaskAlertMod, "AlertMod", stackSize, NULL, LOW_PRIORITY, &TaskAlertMod_Handler);


}


//===============================================================================
//  Main
//===============================================================================


/* 
    TaskRFRecv: Producer | TaskAlertMod: Consumer 
    When TaskRFRecv is receiving HIGH (1) movement,
    TaskAlertMod turns on (resumes) else suspeds 
*/

// PRODUCER: Task will read radio receiver, will write to GLOBAL_ALERT when MOVEMENT is HIGH
void TaskRFRecv(void *pvParameters){

  (void) pvParameters;

  // RF Module configurations
  radio.begin();                     // Start instance of the radio object
  radio.openReadingPipe(0, address); // Setup pipe to read data to the address that was defined
  radio.setPALevel(RF24_PA_HIGH);     // Set the Power Amplified level to [WIP]] in this case
  radio.startListening();            // We are going to be the receiver, so we need to start listening

  // Tasks run indefinitely
  for (;;){

    if (radio.available()) {
      
      // Scoped such as to clear buffer with ease
      bool MOVEMENT;

      radio.read(&MOVEMENT, sizeof(bool));
      
      #ifdef DEBUG_ENABLE
      Serial.print("TaskRFRecv ---- MOVEMENT: "); Serial.println(MOVEMENT);
      #endif

      // Take mutex to write GLOBAL_ALERT = MOVEMENT
      if (xSemaphoreTake(mutex, 10) == pdTRUE){

        #ifdef DEBUG_ENABLE
        Serial.print("TaskRFRecv ---- Taking Mutex, setting GLOBAL_ALERT = MOVEMENT: ");
        Serial.println(MOVEMENT);
        #endif

        GLOBAL_ALERT = MOVEMENT;
        xSemaphoreGive(mutex);
      }


    } // eo if

    vTaskDelay(1);

  } // eo for
}

// CONSUMER: Will turn on alert upon TaskRFRecv HIGH for at least 250 ms and LOW for 125 ms (375 ms total)
void TaskAlertMod(void *pvParameters){

  (void) pvParameters;

  // Alert Module set as Output
  pinMode(BUZZER_PIN, OUTPUT);

  for (;;){

    if (xSemaphoreTake(mutex, 3) == pdTRUE){
      
      // Assign to local status
      bool ALERT_STATUS = GLOBAL_ALERT;

      #ifdef DEBUG_ENABLE
      Serial.println("TaskAlertMod ---- Setting ALERT_STATUS = GLOBAL_ALERT");
      #endif

      // Release
      xSemaphoreGive(mutex);

      if (ALERT_STATUS){
        digitalWrite(BUZZER_PIN, HIGH);
        // vTaskDelay( 250 / portTICK_PERIOD_MS);
      } else {
        digitalWrite(BUZZER_PIN, LOW);
        // vTaskDelay( 125 / portTICK_PERIOD_MS);
      }

  
    } // eo mutex if
  

    vTaskDelay(5); // Prevents tasks from overloading scheduler

  } // eo for
}


// Not utilized (RTOS Tasks instead)
void loop() { }
