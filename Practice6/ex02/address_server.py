import sys
import socket

BUFFER_SIZE = 200

server_addr = sys.argv[1]
server_port = int(sys.argv[2])
CALC_ADDRESS = sys.argv[3].encode()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((server_addr, server_port))

while True:
    try:
        data, client_addr = sock.recvfrom(BUFFER_SIZE)
        if data.decode() == "Hello server":
            print(f"{client_addr[0]}:{client_addr[1]} has asked for the address")
            sock.sendto(CALC_ADDRESS, client_addr)
    except KeyboardInterrupt:
        break
sock.close()