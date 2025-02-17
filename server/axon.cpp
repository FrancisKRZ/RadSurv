#include "axon.h"

// Constructor
TREV::TREV() : addr_len(0), num_addresses(0), address(nullptr), current_status(OFF) {}

// Destructor to free memory
TREV::~TREV() {
    clear_addresses();
}

// Clear dynamically allocated addresses
void TREV::clear_addresses() {

}

// Getter for status
unsigned short TREV::get_status() const {
    return current_status;
}

String TREV::get_message() {
  return message;
}

// Getter for address
byte* TREV::get_address(unsigned short addr_index) const {
    if (addr_index < num_addresses) {
        return address[addr_index];
    }
    return nullptr; // Return nullptr if index is out of bounds
}

// Setter for status
void TREV::set_status(unsigned short status) {
    current_status = static_cast<RF_STATUS>(status);
}

// Setter for address with dynamic memory management
void TREV::set_address(byte* addr, unsigned short num_addr, unsigned short len) {

}


void TREV::set_message(String msg){
  message = msg;
}