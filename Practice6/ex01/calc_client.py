import sys
import socket
import random
import struct
import time

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((server_addr, server_port))

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