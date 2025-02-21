# rf_to_server.py ---- Will be running on an OS such as to make file wr/rd seamless with added bit protection(s)
# An NRF24 module will be loaded into the machine, capture the varios addr signals
# Append the signal readouts to a buffer then write after a certain size and/or time

# This will run in a light MCU , no file operations are to be made to preserve resources

# Libraries as seen in rr-server.py
import argparse
import struct
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
logging.basicConfig(filename="../log/rf_to_server.log", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()


# [MUTEX] Shared Resource Queue <Implementation>: 
class SharedQueue:

    def __init__(self, depth):
        
        self.depth = depth                          # Queue depth limit
        self.count = 0                              # Current item count, starts at 0
        self.rd_ptr = 0
        # All flags are type bool
        # Empty flag , Full flag
        # Almost Empty flag  , Almost Full flag 

        # Queue
        self.queue = [None] * self.depth

    # [Mutex] Acquire and Release mutex during use (caller function) instead of implementation
    def write_data(self, data):

        try:
            if self.get_Full_flag() is False:
                self.queue[count] = data
                self.count = self.count + 1
        except:
            print("Failed SharedQueue write_data")
            logger.error("Error: Device %s Failed SharedQueue write_data", socket.gethostbyname())

    # [Mutex]
    def read_data(self):

        try:
            if self.get_Empty_flag is False:
                self.count = self.count - 1      # Update size counter
                self.rd_ptr = rd_ptr + 1         # Update read pointer prior to return
                return SharedQueue[rd_ptr-1]     # return the original pointed Queue rd
        except:
            print("Failed to read data")
            logger.error("Error: Device %s Failed ShareQueue read_data", socket.gethostbyname())


    # Get Queue item
    def get_queue(self):
        return self.queue

    def get_count(self):
        return self.count

    # Get Queue Buffer status flags
    def get_Full_flag(self):
        return self.count == self.depth
    
    def get_Empty_flag(self):
        return self.count == 0

    def get_AE_flag(self):
        return self.count < self.depth * 0.25

    def get_AF_flag(self):
        return self.count > self.depth * 0.75


# [THREAD] Producer: Builds packet frames from RF data
# The buffer will have an 'almost full' flag, where in >= %75
# of its size is reached will build the frame or if a certain
# amount of time has elapsed [30, 60] seconds and the buffer
# is not empty, will build the frame.
# Additionally, we'll keep track of the devices sending data dynamically
# Payload is in Queue Object
class RFPacketBuilder(Thread):

    def __init__(self, 
        local_hostname, local_port):

        self.local_hostname = local_hostname
        self.local_port = local_port

        # Thread Mutex thingamajig
        Thread.__init__(self)

    # Builds a Packet containing local and remote addrs & port
    # current time, queue and queue's item count
    # <returns struct.pack>
    def build_packet(Queue_Object: SharedQueue):

        # Build Packet containing: Local IDs, Payload metadata, connection metadata...
        print(f"Build object with data: {Queue_Object.queue}")
        
        # Current time as of packet build
        cur_date = datetime.now()
        # SharedQueue queue and item count
        queue = SharedQueue.get_queue()
        count = SharedQueue.get_count()

        packet = struct.pack(local_hostname, local_port, 
                            cur_date, queue, count
                            )

        return packet


# Init should establish TCP connection, we'll simply send and await confirmation
class RFPacketSender(Thread):

    def __init__(self, remote_address, remote_port):
        
        self.remote_address = remote_address
        self.remote_port = remote_port

        # Create Socket connection and Connect to remote server
        self.socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_connection.bind(self.remote_address, self.remote_port)

    def send_packet(Queue_Object):

        print("Sending Packet")
        


if __name__ == "__main__":

    print(f"Server at {socket.gethostbyname()}")

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
    PacketBuilder = RFPacketBuilder(
        local_hostname=local_hostname, local_port=local_port,
        remote_hostname=remote_hostname, remote_port=remote_port,
        Queue_Object=Queue
        )

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
        logger.error("Error during receiver body execution by device %s", socket.gethostbyname())
        traceback.print_exc()
        nrf.power_down()
        pi.stop()
