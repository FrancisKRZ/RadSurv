/* Manages radio addressing and data management */
#ifndef AXON_H
#define AXON_H
#include "AList.h"

class TREV {

private:

    string addresses[];

    void clear_addresses();

public:
    // Constructor
    TREV();

    // Destructor to free memory
    ~TREV();

  

};

#endif