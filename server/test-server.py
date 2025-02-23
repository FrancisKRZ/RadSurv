from server import ServerTCPHandler
from server import Server

# Parse Command Line Arguments
import argparse


def unit_tests():
    pass




if __name__ == "__main__":

    print(f"Host Server running at {socket.gethostbyname()}")

    # Parse command line arguments
    parser = argparse.ArgumentParse(prog="server.py", description="Listens to packets from RF Server nodes.")
    parser.add_argument('-n', '--hostname', type=str, default='localhost', help="Hostname for the Server.")
    parser.add_argument('-p', '--port', type=int, default=8888, help="Port number for Server.")

    args = parser.parse_args()
    hostname = args.hostname
    port = args.port
    maximum_connections = args.maxconns
    message_length = args.messagelength

    server = Server(hostname, port, maximum_connections, message_length)

    print(f"Hostname: {hostname}, listening on port: {port}\
        \nMaximum connections {maximum_connections}, message length: {message_length}")

    server.server_start()
