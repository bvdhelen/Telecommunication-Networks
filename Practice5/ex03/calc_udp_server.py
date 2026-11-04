import socket
import struct
import sys

server_addr = (sys.argv[1], int(sys.argv[2]))

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(server_addr)
    sock.settimeout(1)

    unpacker = struct.Struct("I I 1s")

    while True:
        try:
            data, client = sock.recvfrom(unpacker.size)
            unpacked_data = unpacker.unpack(data)
            
            print(f"Received: {unpacked_data}")

            x = eval(f"{unpacked_data[0]}{unpacked_data[2].decode()}{unpacked_data[1]}")
            x_round = round(x, 3)
            sock.sendto(str(x_round).encode(), client)

        except socket.timeout:
            pass
        except KeyboardInterrupt:
            sock.close()
            break
        except socket.error as msg:
            print(msg)