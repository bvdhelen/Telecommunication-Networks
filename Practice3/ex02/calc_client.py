import socket
import struct

server_addr = ('localhost', 10000)
packer = struct.Struct("I I 1s")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect(server_addr)
    num1 = input("Enter a number: ")
    op = input("Enter an operator: ")
    num2 = input("Enter another number: ")

    packed_data = packer.pack(int(num1), int(num2), op.encode())
    
    client.sendall(packed_data)
    data = client.recv(16).decode()

    print("Result:", data)
