# server.py ---- Responsible for receiving wifi packets from rf_to_server.py
# The packets will contain with address, time, length and contents
# Primary Identifiers: address

# Will be multithreaded; 
# a Producer will obtain the packets from rf_to_server.py
# a Consumer will unpack the structs then add to a database
# after a buffer indicates almost full flag or until some time has passed whilst in buffer

# Runs in a localized server running GNU/Linux
# Sys for files, socket for wireless connection, time for managing file saving parametrization
import sys
import socket
import time

# Multi-Threaded for Server and Radio operations
from threading import Lock, Thread
