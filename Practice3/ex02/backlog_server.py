import socket
import time

server_addr = ('localhost', 10000)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

with sock as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(server_addr)
    server.listen(5)
    server.settimeout(1)
    while True:
        try:
            client, client_addr = server.accept()
            print("Connected:", client_addr)
            time.sleep(10)
        except socket.error:
            pass
        except KeyboardInterrupt:
            sock.close()
            break