# NOTE: https://docs.python.org/3.11/howto/sockets.html

# server.py ---- Responsible for receiving wifi packets from rf_to_server.py
# The packets will contain with address, time, length and contents
# Primary Identifiers: address

# Will be multithreaded; 
# a Producer will obtain the packets from rf_to_server.py
# a Consumer will unpack the structs then add to a database
# after a buffer indicates almost full flag or until some time has passed whilst in buffer

# Runs in a localized server running GNU/Linux
# Socket for wireless connection, time for managing file saving parametrization
import socketserver
import socket
import time

# Parse Command Line Arguments
import argparse
# Log errors to log/ directory
import logging
# Allows to unpack packet as a dictionary
from packet import unpack_packet

# Multi-Threaded for Server spawns
from threading import Lock
from threading import Thread

# Used for handling client threads across processors
# from multiprocessing import Pool # Enable only if required IPC between sockets

# Mutex Lock
mutex = Lock()

# Global Logging Object
logging.basicConfig(filename="../log/server.log", format='%(asctime)s %(message)s', filemode='a')
logger = logging.getLogger()


# TCP Socket Server handler, instanced once per connection to the server,
# overrides the handle() method to implement client communication
class ServerTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        
        # Unpack the data packet
        packet = unpack_packet(self.data)

        print(packet['hostname'])
        print(packet['port'])
        print(packet['queue'])

        # We'll buffer the data, format, then save to database
        pass
        # Send acknowledge request
        self.request.sendall(self.data)


# A wrapper which will enable threaded utilization in the server and allows
# class Server to properly be non-blocking
class ThreadedTCPServer(socketserver.ThreadingTCPServer):
    
    # Avoids "address already in use" errors
    allow_reuse_address = True


# The connection shall be TCP to ensure quality file wr/rd and surveillance integrity
class Server(Thread):

    def __init__(self, hostname, port, MAXIMUM_CONNECTIONS, MESSAGE_LENGTH):
        # Server Address
        self.hostname = hostname
        self.port     = port
        # Maximum connections and expected Message Length
        self.MAXIMUM_CONNECTIONS = MAXIMUM_CONNECTIONS
        self.MESSAGE_LENGTH = MESSAGE_LENGTH
        # Server socket initialization
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allows socket reuse address
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        time.sleep(0.5)
        self.server.bind((self.hostname, self.port))


    def server_start(self):

        try:
            with ThreadedTCPServer((self.hostname, self.port), ServerTCPHandler) as server:
                # Activate server and runs until program interrupt
                server.serve_forever()
        # Catch exception error and log
        except Exception as e:
            logger.error(f"Error during server_start() execution: {e}")


    # Socket impl
    def socket_start(self):

        # Listens up to MAX connections
        self.server.listen(self.MAXIMUM_CONNECTIONS)

        while True:
            # Accepts connections from outside
            (clientsocket, address) = self.server.accept()

    
    # Will change the following function implementations: send(), receive()
    def socket_send(self, msg):

        msg_len = len(msg)
        total_sent = 0

        while total_sent < msg_len:
            try:
                sent = self.server.send(msg[total_sent:])
                total_sent = total_sent + 1
            except:
                logger.error("Server %s socket connection broken", socket.gethostbyname(self.hostname))


    def socket_receive(self):

        msg_chunk = []
        bytes_recv = 0

        while bytes_recv < self.MESSAGE_LENGTH:
            try:
                msg_chunk = self.server.recv(min(self.MESSAGE_LENGTH - bytes_recv, self.MESSAGE_LENGTH))
                msg_chunk.append(msg_chunk)
                bytes_recv = bytes_recv + len(msg_chunk)
            except:
                logger.error("Server %s socket connection broken", socket.gethostbyname(self.hostname))
        
        return b''.join(msg_chunk)



if __name__ == "__main__":



    # Parse command line arguments
    parser = argparse.ArgumentParser(prog="server.py", description="Listens to packets from RF Server nodes.")
    parser.add_argument('-n', '--hostname', type=str, default='localhost', help="Hostname for the Server.")
    parser.add_argument('-p', '--port', type=int, default=8888, help="Port number for Server.")
    parser.add_argument('-m', '--maxconns', type=int, default=5, help="Maximum Server connections from clients.")
    parser.add_argument('-l', '--messagelength', type=int, default=128, help="Message length")

    args = parser.parse_args()
    hostname = args.hostname
    port = args.port
    maximum_connections = args.maxconns
    message_length = args.messagelength

    print(f"Host Server running at {socket.gethostbyname(hostname)}")

    print(f"Hostname: {hostname}, listening on port: {port}\
        \nMaximum connections {maximum_connections}, message length: {message_length}")

    server = Server(hostname, port, maximum_connections, message_length)
    server.server_start()






