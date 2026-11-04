import sys
import socket
import random
import struct
import time

ASK_FOR_ADDRESS_MSG = "Hello server".encode()
BUFFER_SIZE = 200

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.sendto(ASK_FOR_ADDRESS_MSG, (server_addr, server_port))
address, _ = udp_sock.recvfrom(BUFFER_SIZE)
calc_ip, calc_port = address.decode().split(":")
calc_port = int(calc_port)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((calc_ip, calc_port))

ops = ["+", "-", "*", "/"]

packer = struct.Struct("i i 1s")

for nrnd in range(5):
    operand_a = random.randint(1, 100)
    operand_b = random.randint(1, 100)
    operator = random.choice(ops)

    msg = packer.pack(operand_a, operand_b, operator.encode())
    print(f"Message: {operand_a} {operator} {operand_b}")
    sock.sendall(msg)

    msg = sock.recv(packer.size)
    parsed_msg = packer.unpack(msg)
    print(f"Received result: {parsed_msg[0]}")
    time.sleep(2)
sock.close()
