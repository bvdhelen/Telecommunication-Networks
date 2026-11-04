import sys
import socket
import struct

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

ops = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: int(x / y),
}

packer = struct.Struct("i i c")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server: #IPv4, UDP
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.settimeout(1)
    server.bind((server_addr, server_port))

    while True:
        try:
            data, client_addr = server.recvfrom(packer.size)
            parsed_msg = packer.unpack(data)
            result = ops[parsed_msg[2].decode()](parsed_msg[0], parsed_msg[1])
            msg = packer.pack(result, 0, b"R")
            server.sendto(msg, client_addr)
        except KeyboardInterrupt:
            pass
        except socket.timeout:
            pass    
server.close()
