import socket
import time

server_addr = ('localhost', 10000)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

with sock as client:
    print("Connecting")
    try:
        client.connect(server_addr)
        print("Connected")
        time.sleep(100)
    except KeyboardInterrupt:
        sock.close()