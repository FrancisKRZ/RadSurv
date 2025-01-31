#ifndef AXON_H
#define AXON_H

#include <Arduino.h>
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>


// Byte Definition
#define byte unsigned char

class TREV {

private:
    unsigned short addr_len;
    unsigned short num_addresses;
    byte** address; // Dynamically allocated 2D array

    enum RF_STATUS { OFF, READING, WRITING };
    RF_STATUS current_status;

    String message;

    void clear_addresses();

public:
    // Constructor
    TREV();

    // Destructor to free memory
    ~TREV();

    // Getter for status
    unsigned short get_status() const;

    // Getter for address
    byte* get_address(unsigned short addr_index) const;

    String get_message();

    // Setter for status
    void set_status(unsigned short status);

    // Setter for address with dynamic memory management
    void set_address(byte* addr, unsigned short num_addr, unsigned short len);

    // Set message
    void set_message(String msg);

};

#endif