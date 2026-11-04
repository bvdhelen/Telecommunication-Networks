import socket
import sys
import time

TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])
BUFFER_SIZE = 1024
MESSAGE = "Hello server".encode()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((TCP_IP, TCP_PORT))
    for i in range(6):
        sock.sendall(MESSAGE)
        print("Sent message:", MESSAGE)
        reply = sock.recv(BUFFER_SIZE)
        print("Response:", reply.decode())

        time.sleep(10)