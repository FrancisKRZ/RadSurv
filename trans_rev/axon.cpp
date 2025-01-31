#include "axon.h"

// Constructor
TREV::TREV() : addr_len(0), num_addresses(0), address(nullptr), current_status(OFF) {}

// Destructor to free memory
TREV::~TREV() {
    clear_addresses();
}

// Clear dynamically allocated addresses
void TREV::clear_addresses() {
    if (address) {
        for (unsigned short i = 0; i < num_addresses; ++i) {
            delete[] address[i];
        }
        delete[] address;
        address = nullptr;
        num_addresses = 0;
        addr_len = 0;
    }
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
    clear_addresses(); // Free existing addresses

    if (num_addr > 0 && len > 0) {
        addr_len = len;
        num_addresses = num_addr;
        address = new byte*[num_addresses];
        for (unsigned short i = 0; i < num_addresses; ++i) {
            address[i] = new byte[addr_len];
            memcpy(address[i], addr, addr_len * sizeof(byte));
        }
    }
}


void TREV::set_message(String msg){
  message = msg;
}