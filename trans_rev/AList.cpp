// Implementation of the ADT List using array
#include "AList.h"

AList::~AList() { delete [] listArray; }

int AList::getMaxSize() const{
    return maxSize;
}

// Reinitialize the list
void AList::clear() { listSize = curr = 0; }

void AList::resize() {
    maxSize = maxSize * 2;
    ListItemType *tmp = new ListItemType[maxSize];

    for(int i = 0; i < listSize; i++) tmp[i] = listArray[i];

    delete [] listArray;
    listArray = tmp;
}

// Insert "it" at current position
bool AList::insert(const ListItemType& it) {
    if (listSize >= maxSize) resize();

    // Shift elements right to make room
    for (int i = listSize; i > curr; i--)
        listArray[i] = listArray[i-1];
    listArray[curr] = it;
    listSize++;
    return true;
}

// Append "it" to list
bool AList::append(const ListItemType& it) {
    if (listSize >= maxSize) resize();

    listArray[listSize++] = it;
    return true;
}

// Remove and return the current element
ListItemType AList::remove() {
    if ((curr < 0) || (curr >= listSize)) // No current element
        throw std::out_of_range("remove() in AList has current of " + std::to_string(curr) + " and size of "
                                + std::to_string(listSize) + " that is not a a valid element");
    ListItemType it = listArray[curr];     // Copy the element
    for(int i = curr; i < listSize-1; i++) // Shift them down
        listArray[i] = listArray[i+1];
    listSize--;                            // Decrement size
    return it;
}

void AList::moveToStart() { curr = 0; }       // Set to front
void AList::moveToEnd() { curr = listSize; }  // Set at end
void AList::prev() { if (curr != 0) curr--; } // Move left
void AList::next() { if (curr < listSize) curr++; } // Move right
int AList::length() const { return listSize; }       // Return list size
int AList::currPos() const { return curr; }          // Return current position

// Set current list position to "pos"
bool AList::moveToPos(int pos) {
    if ((pos < 0) || (pos > listSize)) return false;
    curr = pos;
    return true;
}

// Return true if current position is at end of the list
bool AList::isAtEnd() const { return curr == listSize; }

// Return the current element
ListItemType AList::getValue() const {
    if ((curr < 0) || (curr >= listSize)) // No current element
        throw std::out_of_range("getvalue() in AList has current of " + std::to_string(curr) +  + " and size of "
                                + std::to_string(listSize) + " that is not a a valid element");
    return listArray[curr];
}

// Check if the list is empty
bool AList::isEmpty() const { return listSize == 0; }

// Returns a string of the list representation in the format < _,_|_>
// <1,2|3>
string AList::to_string() const {
    string res = "<";
    int i;
    for (i = 0; i < listSize; i++) {
        if ( i == curr) res += "|";
        res += std::to_string(listArray[i]);
        if (i != listSize -1 && curr != i + 1)  res += ",";
    }
    if ( i == curr) res += "|";
    res += ">";
    return res;

    return "";
}


// Returns amount of times the int 'it' appears in the list
int AList::count(const ListItemType &it) const{

    int ctr = 0;
    for (int i = 0; i < listSize; i++) if (listArray[i] == it) ctr++;

    return ctr;
}


// Eliminates zeroes from the list
// check if index number is zero, if true then use remove()
// to eliminate it & shift all numbers left.
void AList::elimZeros(){

    int ctr = 0, n = 0;

    for (int i = 0; i < listSize; i++){
        if (listArray[i] != 0) listArray[ctr++] = listArray[i];
        else n++;
    }

    listSize -= n;
}


// Appends the invoking list with 'other' list, w/o using existing append function
// This resizes using the listSize of both arrays, else it'll be filled with garbage
// Then it adds to the space with the index being the size of the other array
void AList::append(const AList &other){

    if (listSize + other.listSize > maxSize){
        maxSize = listSize + other.listSize;

        ListItemType *tmp = new ListItemType[maxSize];

        for (int i = 0; i < listSize; i++){
            tmp[i] = listArray[i];
        }
        delete [] listArray;
        listArray = tmp;

    }

    for (int k = 0; k < other.listSize; k++){
        listArray[listSize+k] = other.listArray[k];
    }

    listSize += other.listSize;

}

// Rotates list, <|1 , 2 , 3> rotate(1)  <|3, 1, 2>
void AList::rotate(const int k){

    int i;
    ListItemType rList[listSize];

    for (i = 0; i < listSize; i++) rList[ (i + k) % listSize ] = listArray[i];

    for (i = 0; i < listSize; i++) listArray[i] = rList[i];

}


// Checks if all numbers are between a min and a max (a , b)  element is >= a && element is <= b
bool AList::contains_all(int a, int b) const{

    for (int i = 0; i < listSize; i++){
        if ( !( listArray[i] >= a && listArray[i] <= b )) return false;
    }

    return true;
}


// Return random, returns a random number from the list and decrements the list by 1, O(1)
ListItemType AList::random(){

    ListItemType num;
    srand(time(NULL));

    swap(listArray[ (rand() % listSize-1) + 1 ], listArray[listSize-1]);
    num = listArray[listSize-1];
    listSize--;

    return num;
}


// returns true if invoking and other are same size and
// has the same values in the same indexes
// else its false
// current position doesnt matter, nor maxSize.
// A.operator==(B)
bool AList::operator == (const AList &other) const{

    if (listSize != other.listSize) return false;

    // element comparison

    for (int i = 0; i < listSize; i++){
        if ( listArray[i] != other.listArray[i] ) return false;
    }
    return true;
}



// Returns true if invoking object's array is smaller than other
// <1,2,3>   <    <0,1,2,3,4>   returns true
//bool AList::operator < (const AList &other) const{
//    return listSize < other.listSize;
//}


// Returns true if the sum of elements of the invoking object is
// less than sum of elements in the other object.

//bool AList::operator < (const AList &other) const{

//    ListItemType sumA = 0, sumB = 0;

//    for (int i = 0; i < listSize; i++) sumA += listArray[i];
//    for (int k = 0; k < other.listSize; k++) sumB += other.listArray[k];

//    return sumA < sumB;
//}


bool AList::operator<(const AList &other) const{

    int SIZE = listSize + other.listSize;

    for (int i = 0; i < SIZE; i++){
        if (listArray[i] > other.listArray[i]) return false;
    }

    return true;
}

// Returns true if all elements of A is greater than all of B
// i.e    A = < 5 , 15 , 35 >    B = < 10, 20, 30 >
//          A is greater because 35 > 30
bool AList::operator > (const AList &other) const{

    int maxA = listArray[0], maxB = other.listArray[0];

    for (int i = 1; i < listSize; i++)          if (listArray[i-1] < listArray[i]) maxA = listArray[i];
    
    for (int k = 1; k < other.listSize; k++)    if (other.listArray[k-1] < other.listArray[k]) maxB = other.listArray[k];

    return maxA > maxB;

}






