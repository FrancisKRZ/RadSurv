import socket

from SharedQueue import SharedQueue
from rfserver import RFPacketBuilder
from rfserver import RFPacketSender
from packet import build_packet

# Parse Command Line Arguments
import argparse



def unit_tests(remote_hostname, remote_port, local_hostname, local_port, packet: bytes):
   
    pass




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

    # SharedQueue Buffer
    buffer = SharedQueue(10)

    for i in range (10):
        buffer.write_data(i*10)

    # struct.pack -> bytes

    print(f"Buffer count: {buffer.get_count()}")

    packet = build_packet(local_hostname, local_port, buffer)

    socket = RFPacketSender(remote_hostname, remote_port)
    socket.connect()
    socket.send(packet)
    socket.close_socket()
