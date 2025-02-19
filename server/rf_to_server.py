# rf_to_server.py ---- Will be running on an OS such as to make file wr/rd seamless with added bit protection(s)
# An NRF24 module will be loaded into the machine, capture the varios addr signals
# Append the signal readouts to a buffer then write after a certain size and/or time

# This will run in a light MCU , no file operations are to be made to preserve resources

# Libraries as seen in rr-server.py
import argparse
import struct # for unpacking packets
import traceback

# Pi Zero GPIO 
import pigpio

# NRF24 Python Library by bjarne-hansen
from nrf24 import *

import sys
import socket
import time

# Log critical error events from SharedQueue wr/rd, Radio failures and Socket wr operations
import logging

# Multi-Threaded for Server and Radio operations
from threading import Lock
from threading import Thread

mutex = Lock()

# Global Logging Object
logging.basicConfig(filename="rf_to_server.log", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()


# [MUTEX] Shared Resource Queue <Implementation>: 
class SharedQueue:

    def __init__(self, depth):
        
        self.depth = depth                          # Queue depth limit
        self.count = 0                              # Current item count, starts at 0
        # All flags are type bool
        # Empty flag , Full flag
        # Almost Empty flag  , Almost Full flag 

        # Queue
        self.queue = [None] * self.depth

    def write_data(self, data):

        try:
            if self.get_Full_flag() is False:
                self.queue[count] = data
                count = count + 1
        except:
            # CR - Mutex
            mutex.acquire()
            print("Failed SharedQueue write_data")
            logger.error("Error: Device %s Failed SharedQueue write_data", socket.gethostbyname())
            mutex.release()

    # Get Queue Buffer status flags
    def get_Full_flag(self):
        return self.count == self.depth
    
    def get_Empty_flag(self):
        return self.count == 0

    def get_AE_flag(self):
        return self.count < self.depth * 0.50

    def get_AF_flag(self):
        return self.count >= self.depth * 50


# [THREAD] Producer: Builds packet frames from RF data
# The buffer will have an 'almost full' flag, where in >= %75
# of its size is reached will build the frame or if a certain
# amount of time has elapsed [30, 60] seconds and the buffer
# is not empty, will build the frame.
# Additionally, we'll keep track of the devices sending data dynamically
class RFPacketBuilder(Thread):

    def __init__(self, 
        server_hostname, server_port, 
        client_hostname, client_port, cur_time, payload):

        self.server_hostname = server_hostname
        self.server_port = server_port
        self.client_hostname = client_hostname
        self.client_port = client_port
        self.cur_time = cur_time
        self.payload = payload

        Thread.__init__(self)

    ''




if __name__ == "__main__":

    print(f"Server at {socket.gethostbyname()}")

    # Parse command line arguments
    parser = argparse.ArgumentParser(prog="rf_to_server.py", description="Simple NRF24 Request/Response Server Example.")
    parser.add_argument('-n', '--hostname', type=str, default='localhost', help="Hostname for the RF Node running the pigpio daemon.")
    parser.add_argument('-p', '--port', type=int, default=8888, help="Port number of the pigpio daemon.")
    parser.add_argument('address', type=str, nargs='?', default='1SRVR', help="Radio Address to listen to (up to 6 ASCII characters).")


    # Address Char Limit
    ADDRESS_CHAR_LIMIT = 6

    args = parser.parse_args()
    hostname = args.hostname
    port = args.port
    address = args.address


    # Open log file


    # Check if addr is not char [6]
    if (len(address) >= ADDRESS_CHAR_LIMIT):
        print(f'Invalid address {address} ---- {len(address)} >= {ADDRESS_CHAR_LIMIT}')
        sys.exit(1)
    

    # Connect to pigpiod
    print(f'Connecting to GPIO daemon on {hostname}:{port} ...')
    pi = pigpio.pi(hostname, port)
    if not pi.connected:
        print(f"Not connected to {hostname}")
        sys.exit()

    # NRF24 Object
    nrf = NRF24(pi, ce=25, payload_size=RF24_PAYLOAD.DYNAMIC, channel=100, 
                data_rate=RF24_DATA_RATE.RATE_250KBPS, pa_level=RF24_PA.HIGH)
    
    nrf.set_address_bytes(len(address))

    # Display the content of NRF24L01 device registers.
    nrf.show_registers()

    
    # Receiver body
    try:
        print(f"Receiving from {address}")
        
        while True:
            # Listening on parameter addr
            nrf.open_reading_pipe(RF24_RX_ADDR.P1, address)

            while nrf.data_ready():

                # Time of reception
                cur_date = datetime.now()

                # Read pipe and payload message
                pipe = nrf.data_pipe()
                payload = nrf.get_payload()

                # Protocol number
                protocol = payload[0] if len(payload) > 0 else -1

                # Print message
                print(f"{cur_date:%Y-%m-%d %H:%M:%S.%f}: pipe {pipe}, len: {len(payload)}")

                # Delay 1 ms
                time.sleep(0.001)

    except:
        # If catch exception, power down device(s)
        traceback.print_exc()
        nrf.power_down()
        pi.stop()
