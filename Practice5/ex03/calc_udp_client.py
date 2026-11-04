import socket
import struct
import sys
import random
import time

server_addr = (sys.argv[1], int(sys.argv[2]))

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    packer = struct.Struct("I I 1s")

    for _ in range(10):
        num1 = random.randint(1, 100)
        op = random.choice("+-/*").encode()
        num2 = random.randint(1, 100)

        packed_data = packer.pack(num1, num2, op)
        
        sock.sendto(packed_data, server_addr)
        data, _ = sock.recvfrom(16)

        print(f"Result: {data.decode()}")
        time.sleep(2)
