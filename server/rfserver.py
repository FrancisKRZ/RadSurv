# rf_to_server.py ---- Will be running on an OS such as to make file wr/rd seamless with added bit protection(s)
# An NRF24 module will be loaded into the machine, capture the varios addr signals
# Append the signal readouts to a buffer then write after a certain size and/or time

# This will run in a light MCU , no file operations are to be made to preserve resources

# Libraries as seen in rr-server.py
import argparse
import traceback

from packet import build_packet

# Pi Zero GPIO 
import pigpio

# NRF24 Python Library by bjarne-hansen
from nrf24 import *

import sys
import socket

import time
from datetime import datetime

# SharedQueue buffer
import SharedQueue

# Log critical error events from SharedQueue wr/rd, Radio failures and Socket wr operations
import logging

# Multi-Threaded for Server and Radio operations
from threading import Lock
from threading import Thread

mutex = Lock()

# Global Logging Object
logging.basicConfig(filename="../log/rfserver.log", format='%(asctime)s %(message)s', filemode='a')
logger = logging.getLogger()





# [THREAD] Producer: Builds packet frames from RF data
# The buffer will have an 'almost full' flag, where in >= %75
# of its size is reached will build the frame or if a certain
# amount of time has elapsed [30, 60] seconds and the buffer
# is not empty, will build the frame.
# Additionally, we'll keep track of the devices sending data dynamically
# Payload is in Queue Object

# Returns a struct pack containing local hostname, local port
# queue list and queue length
class RFPacketBuilder(Thread):

    def __init__(self, local_hostname: str, local_port: int):
        # Local Device
        self.local_hostname = local_hostname
        self.local_port = local_port

        # Thread Mutex thingamajig
        Thread.__init__(self)

    pass
    # Manage packets using packet.py

# Init should establish TCP connection, we'll simply send and await confirmation
class RFPacketSender(Thread):

    def __init__(self, remote_hostname: str, remote_port: int):        
        # Remote Device
        self.remote_hostname = remote_hostname
        self.remote_port = remote_port
        self.client = None

    # Connect to remote server
    def connect(self):

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.client:
                # Connects client to server
                self.client.connect((self.remote_hostname, self.remote_port))
        except Exception as e:
            logger.error(f"Error during RFPacketSender.connect(): {e}")

    # Safely close socket connection
    def close_socket(self):
        
        try:
            self.client.shutdown()
            self.client.close()
        except Exception as e:
            logger.error(f"Error during RFPacketSender close_socket(): {e}")


    def send(self, packet : bytes):
        
        try:
            self.client.sendall(packet)
        except Exception as e:
            logger.error(f"Error during RFPacketSender.send(): {e}")


    def receive(self):

        try:
            recv = str(self.client.recv(1024), "utf-8")
        except Exception as e:
            logger.error(f"Error during RFPacketSender.receive(): {e}")



# Calls arg parser, pigpio, rf module, and manages SharedQueue buffer wr/rx and socket connection(s)
if __name__ == "__main__":


    # Parse command line arguments
    parser = argparse.ArgumentParser(prog="rf_to_server.py", description="Simple NRF24 Request/Response Server Example")
    
    # Local Device Hostname and Port
    parser.add_argument('-n', '--hostname', type=str, default='localhost', help="Hostname for the RF Node running the pigpio daemon")
    parser.add_argument('-p', '--port', type=int, default=8888, help="Port number of the pigpio daemon")

    # Remote Device Hostname and Port
    parser.add_argument('-t', '--remote_hostname', type=str, default='remotehost', help="Hostname for remote server")
    parser.add_argument('-g', '--remote_port', type=int, default=8888, help="Port number of the remote server")

    # Radio Device Transmitter address
    parser.add_argument('-a', '--address', type=str, nargs='?', default='1SRVR', help="Radio Address to listen to (up to 6 ASCII characters)")


    # Address Char Limit
    ADDRESS_CHAR_LIMIT = 6

    # Parse CLI arguments
    args = parser.parse_args()

    # Local device
    local_hostname = args.hostname
    local_port = args.port

    # Remote device
    remote_hostname = args.remote_hostname
    remote_port = args.remote_port

    # RF address
    address = args.address

    print(f"Server at {socket.gethostbyname(local_hostname)}")

    # Check if addr is not char [6]
    if (len(address) >= ADDRESS_CHAR_LIMIT):
        print(f'Invalid address {address} ---- {len(address)} >= {ADDRESS_CHAR_LIMIT}')
        sys.exit(1)
    

    # Connect to pigpiod
    print(f'Connecting to GPIO daemon on {local_hostname}:{local_port} ...')
    pi = pigpio.pi(local_hostname, local_port)
    if not pi.connected:
        print(f"Not connected to {local_hostname}")
        sys.exit()

    # NRF24 Object
    nrf = NRF24(pi, ce=25, payload_size=RF24_PAYLOAD.DYNAMIC, channel=100, 
                data_rate=RF24_DATA_RATE.RATE_250KBPS, pa_level=RF24_PA.HIGH)
    
    nrf.set_address_bytes(len(address))
    # Display the content of NRF24L01 device registers.
    nrf.show_registers()

    # GPIO and RF Initialization completed

    # Maximum Queue depth
    QUEUE_DEPTH = 32

    # Create SharedQueue object
    Queue = SharedQueue(QUEUE_DEPTH)

    # Create RFPacketBuilder object
    PacketBuilder = RFPacketBuilder(local_hostname, local_port)

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

                print(f"Payload: {payload}")
                # Write Packet into SharedQueue
                Queue.write_data(payload)


                # [Mutex and Thread]
                # Send Packet through network & confirm reception after buffer indicates <High Activity>
                # or if 5 minutes has elapsed since buffer item was written <Low Activity>
                if Queue.almost_full() is True:
                    PacketBuilder.build_packet()
                

                # [Mutex and Thread]
                # If a Packet was built, send packet

                # Log total packets sent through network every 30 minutes 
                # or if an anomalous packet amount has been reached




                # Print message
                print(f"{cur_date:%Y-%m-%d %H:%M:%S.%f}: pipe {pipe}, len: {len(payload)}")

                # Delay 1 ms
                time.sleep(0.001)

    except:
        # If catch exception, power down device(s)
        logger.error("Error during receiver body execution by device %s", socket.gethostbyname(local_hostname))
        traceback.print_exc()
        nrf.power_down()
        pi.stop()
