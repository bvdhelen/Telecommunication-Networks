import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4, TCP

server_addr = ('localhost', 10000)
unpacker = struct.Struct("I I 1s") # int, int char[1]

with sock as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #para reutilizar el puerto
    server.bind(server_addr)
    server.listen(1)
    server.settimeout(1)
    while True:
        try:
            client, client_addr = server.accept()
            print("Connected:", client_addr)

            data = client.recv(unpacker.size)
            print("Received:", data)

            unp_data = unpacker.unpack(data)
            print("Unpack:", unp_data)

            x = eval(f"{unp_data[0]}{unp_data[2].decode()}{unp_data[1]}")
            client.sendall(str(x).encode())

        except socket.timeout:
            pass
        except KeyboardInterrupt:
            sock.close()
            break