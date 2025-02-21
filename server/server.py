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

# Used for handling client threads across processors
from multiprocessing import Pool

# Mutex Lock
mutex = Lock()

# Global Logging Object
logging.basicConfig(filename="../log/server.log", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()

# The connection shall be TCP to ensure quality file wr/rd and surveillance integrity
class Server(Thread):

    def __init__(self, hostname, port, MAXIMUM_CONNECTIONS, MESSAGE_LENGTH):
        self.hostname = hostname
        self.port     = port
        self.MAXIMUM_CONNECTIONS = MAXIMUM_CONNECTIONS

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.hostname, self.port)


        self.MESSAGE_LENGTH = MESSAGE_LENGTH

    def start(self):

        # Listens up to MAX connections
        self.server.listen(self.MAXIMUM_CONNECTIONS)

        while True:

            # Accepts connections from outside
            (clientsocket, address) = self.server.accept()

    
    # Will change the following function implementations: send(), receive()
    def send(self, msg):

        msg_len = len(msg)
        total_sent = 0

        while total_sent < msg_len:

            try:
                sent = self.server.send(msg[total_sent:])
                total_sent = total_sent + 1
            except:
                logger.error("Server %s socket connection broken", socket.gethostbyname())


    def receive(self):

        msg_chunk = []
        bytes_recv = 0

        while bytes_recv < self.MESSAGE_LENGTH:
            
            try:
                msg_chunk = self.server.recv(min(self.MESSAGE_LENGTH - bytes_recv, self.MESSAGE_LENGTH))
                msg_chunk.append(msg_chunk)
                bytes_recv = bytes_recv + len(msg_chunk)
            except:
                logger.error("Server %s socket connection broken", socket.gethostbyname())
        
        return b''.join(msg_chunk)


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


