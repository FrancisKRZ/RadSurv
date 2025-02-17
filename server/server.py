# Server ---- Will be running on an OS such as to make file wr/rd seamless with added bit protection(s)
# An NRF24 module will be loaded into the machine, capture the varios addr signals
# Append the signal readouts to a buffer then write after a certain size and/or time

# Sys for files, socket for wireless connection, time for managing file saving parametrization
import sys
import socket
import time

# Multi-Threaded for Server and Radio operations
from threading import Lock, Thread


