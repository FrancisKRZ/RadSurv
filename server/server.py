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

import argparse
import logging

# Multi-Threaded for Server and Radio operations
from threading import Lock
from threading import Thread

mutex = Lock()

# Global Logging Object
logging.basicConfig(filename="../log/server.log", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()

# The connection shall be TCP to ensure quality file wr/rd and surveillance integrity

if __name__ == "__main__":

    print(f"Host Server running at {socket.gethostbyname()}")

    # Parse command line arguments
    parser = argparse.ArgumentParse(prog="server.py", description="Listens to packets from RF Server nodes.")
    parser.add_argument('-n', '--hostname', type=str, default='localhost', help="Hostname for the Server.")
    parser.add_argument('-p', '--port', type=int, default=8888, help="Port number for Server.")

    args = parser.parse_args()
    hostname = args.hostname
    port = args.port

    print(f"Hostname: {hostname}, listening on port: {port}")


