#ifndef CATCHEXAMPLE_ALIST_H
#define CATCHEXAMPLE_ALIST_H
#include "List.h"
#include <stdexcept>
// #include <string>
// #include <iostream>
// #include <ctime>
// #include <cstdlib>
using namespace std;

class AList : public List {
private:
    ListItemType* listArray;            // Array holding list elements
    static const int DEFAULT_SIZE = 10; // Default size
    int maxSize;                        // Maximum size of list
    int listSize;                       // Current # of list items
    int curr;                           // Position of current element

    // Duplicates the size of the array pointed to by listArray
    // and update the value of maxSize.
    void resize();
public:
    int getMaxSize() const;
    // Constructors
    // Create a new list object with maximum size "size"
    AList(int size = DEFAULT_SIZE) : listSize(0), curr(0) {
        maxSize = size;
        listArray = new ListItemType[size];         // Create listArray
    }

    ~AList();     // destructor to remove array

    // Reinitialize the list
    void clear();  // Simply reinitialize values

    // Insert "it" at current position
    bool insert(const ListItemType& it) ;

    // Append "it" to list
    bool append(const ListItemType& it);

    // Remove and return the current element
    ListItemType remove();

    void moveToStart();       // Set to front
    void moveToEnd();         // Set at end
    void prev();              // Move left
    void next();              // Move right
    int length() const;       // Return list size
    int currPos() const;      // Return current position

    // Set current list position to "pos"
    bool moveToPos(int pos);

    // Return true if current position is at end of the list
    bool isAtEnd() const;

    // Return the current element
    ListItemType getValue() const;

    // Check if the list is empty
    bool isEmpty() const;


    string to_string() const;

    // Returns amount of times the int 'it' appears in the list
    int count(const ListItemType &it) const;

    // Eliminates zeroes from the list
    void elimZeros();

    // Appends the invoking list with 'other' list, w/o using existing append function
    void append(const AList &other);

    // Rotate list
    void rotate(const int k);

    // Checks if all numbers are between a min and a max (a , b)  element is >= a && element is <= b
    bool contains_all(int a, int b) const;

    // Return random, returns a random number from the list and decrements the list by 1, O(1)
    ListItemType random();

    // Overload the ' == ' operator
    bool operator == (const AList &other) const;

    // Overload the ' < ' operator
    bool operator < (const AList &other) const;

    // Overload the ' > ' operator
    bool operator > (const AList &other) const;
};


#endif //CATCHEXAMPLE_ALIST_H