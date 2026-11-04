import socket
import sys

#server_addr = ('localhost', 10000)
server_addr = (sys.argv[1], int(sys.argv[2]))
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4, TCP
client.connect(server_addr)

client.sendall("Hello Server!".encode())
data = client.recv(16)
print("Received:", data.decode())

client.close()
