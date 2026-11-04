import socket
import struct
import sys
import time

multicast_group = '224.1.1.1'
server_address = ('', 10000)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)
sock.settimeout(1.0)

# Tell the operating system to add the socket to the multicast group on all interfaces
group = socket.inet_aton(multicast_group)   # Convert an IPv4 address from dotted-quad string format (for example, '123.45.67.89') to 32-bit packed binary format
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)  # ip is interface parameter

# Receive/respond loop
while True:
    try:
        print('\nwaiting to receive message')
        data, address = sock.recvfrom(1024)

        print('received %s bytes from %s: %s' % (len(data), address, data.decode()))
        time.sleep(1.0)
        print('sending acknowledgement to', address)
        sock.sendto('ack'.encode(), address)
    
    except socket.timeout:
        pass
    except KeyboardInterrupt:
        sock.close()
        break