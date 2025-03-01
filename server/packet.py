import struct
from SharedQueue import SharedQueue

# Builds packet containing local hostname & port
# date and queue objects
def build_packet(self, hostname: str, port: int, Queue_Object: SharedQueue) -> bytes:

    # Encode for struct pack
    hostname_bytes = hostname.encode('utf-8')
    hostname_len   = len(hostname_bytes)

    # SharedQueue queue and item count
    queue        = Queue_Object.get_queue()
    queue_length = Queue_Object.get_count()

    # Time as of packing
    cur_date = "{:%B, %d, %Y}".format(datetime.now())
    date_bytes = cur_date.encode('utf-8')
    date_len = len(date_bytes)

    # Packing format: Little Endian Hs[]HHs[]Hh[]
    packetformat = f'<H{hostname_len}sHH{date_len}sH{queue_length}h'

    packet = struct.pack(packetformat, 
                        hostname_len, hostname_bytes, 
                        local_port, 
                        date_len, date_bytes, 
                        queue_length, *queue)

    return packet


def unpack_packet(packet: bytes):
    
    # Unpack hostname length
    hostname_len = struct.unpack_from('<H', packet, 0)[0]
    offset = 2

    # Unpack hostname
    hostname = struct.unpack_from(f'<{hostname_len}s', packet, offset)[0].decode('utf-8')
    offset += hostname_len

    # Unpack port
    port = struct.unpack_from('<H', packet, offset)[0]
    offset += 2

    # Unpack date length
    date_len = struct.unpack_from('<H', packet, offset)[0]
    offset += 2

    # Unpack date
    date = struct.unpack_from(f'<{date_len}s', packet, offset)[0].decode('utf-8')
    offset += date_len

    # Unpack queue length
    queue_length = struct.unpack_from('<H', packet, offset)[0]
    offset += 2

    # Unpack queue items
    queue = list(struct.unpack_from(f'<{queue_length}h', packet, offset))

    return {
        'hostname': hostname,
        'port': port,
        'date': date,
        'queue_length': queue_length,
        'queue': queue
    }