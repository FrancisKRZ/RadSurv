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

# Multi-Threaded for Server and Radio operations
from threading import Lock, Thread


if __name__ == "__main__":

    print(f"Server at {socket.gethostname()}")

    # [WIP] transmitter addr char [6] 000001
    tr_addr = "000001"

    # Parse command line argument.
    parser = argparse.ArgumentParser(prog="rr-server.py", description="Simple NRF24 Request/Response Server Example.")
    parser.add_argument('-n', '--hostname', type=str, default='localhost', help="Hostname for the Raspberry running the pigpio daemon.")
    parser.add_argument('-p', '--port', type=int, default=8888, help="Port number of the pigpio daemon.")
    parser.add_argument('address', type=str, nargs='?', default='1SRVR', help="Address to listen to (3 to 5 ASCII characters).")

    args = parser.parse_args()
    hostname = args.hostname
    port = args.port
    address = args.address

    # Check if addr is not char [6]
    if (len(address) != 6):
        print(f'Invalid address {address} ---- Must correspond to char [6] as transmitter is defined')
        sys.exit(1)
    

    # Connect to pigpiod
    print(f'Connecting to GPIO daemon on {hostname}:{port} ...')
    pi = pigpio.pi(hostname, port)
    if not pi.connected:
        print(f"Not connected to {hostname}")
        sys.exit()

    # NRF24 Object
    nrf = NRF24(pi, ce=25, payload_size=RF24_PAYLOAD.DYNAMIC, channel=100, data_rate=RF24_DATA_RATE.RATE_250KBPS, pa_level=RF24_PA.HIGH)
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

                # Protocol number
                protocol = payload[0] if len(payload) > 0 else -1

                # Print message
                print(f"{now:%Y-%m-%d %H:%M:%S.%f}: pipe {pipe}, len: {len(payload)}")

                # Delay 1 ms
                time.sleep(0.001)


    except:
        # If catch exception, power down device(s)
        traceback.print_exc()
        nrf.power_down()
        pi.stop()
