import socket
import sys
import struct
import time
import random

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

packer = struct.Struct("i i 1s")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    try:
        client.connect((server_addr, server_port))

        ops = ["+", "-", "*", "/"]
        packer = struct.Struct("i i 1s")

        for _ in range(5):
            operand_a = random.randint(1, 100)
            operand_b = random.randint(1, 100)
            operator = random.choice(ops)

            msg = packer.pack(operand_a, operand_b, operator.encode())
            print(f"Message: {operand_a} {operator} {operand_b}")
            client.sendall(msg)
            msg = client.recv(packer.size)
            parse_msg = packer.unpack(msg)
            print(f"Received result: {parse_msg[0]}")
            time.sleep(2)
    except KeyboardInterrupt:
        client.close()
