import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock: # UDP client
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('localhost', 10001)
    sock.bind(server_address)
    sock.settimeout(1.0)

    while True:
        try:
            data, client = sock.recvfrom(200)

            print(f"Received: {data.decode()} (from: {client})")

            sock.sendto(b"Hello client!", client)
        except socket.timeout:
            pass
        except socket.error as msg:
            print(msg)
