# NOTE: https://docs.python.org/3.11/howto/sockets.html

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
class Server(Thread):

    def __init__(self, hostname, port, MAXIMUM_CONNECTIONS):
        self.hostname = hostname
        self.port     = port
        self.MAXIMUM_CONNECTIONS = MAXIMUM_CONNECTIONS

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.hostname, self.port)

    def start(self):

        # Listens up to MAX connections
        self.server.listen(self.MAXIMUM_CONNECTIONS)

        while True:

            # Accepts connections from outside
            (clientsocket, address) = self.server.accept()

            # OFFICIAL DOC ---- NOTE: WE WILL HANDLE CONNECTIONS BY MAKING CHILD THREADS
            '''
            There’s actually 3 general ways in which this loop could work - dispatching a thread to handle clientsocket, 
            create a new process to handle clientsocket, or restructure this app to use non-blocking sockets, 
            and multiplex between our “server” socket and any active clientsockets using select. More about that later. 
            The important thing to understand now is this: this is all a “server” socket does. It doesn’t send any data. 
            It doesn’t receive any data. It just produces “client” sockets. Each clientsocket is created in response to 
            some other “client” socket doing a connect() to the host and port we’re bound to. As soon as we’ve created 
            that clientsocket, we go back to listening for more connections. The two “clients” are free to chat it up -
            they are using some dynamically allocated port which will be recycled when the conversation ends.
            '''



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


