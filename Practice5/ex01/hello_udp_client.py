import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock: # UDP client
    server_address = ("localhost", 10001)

    try:
        sock.sendto(b"Hello server!", server_address)
        data, _ = sock.recvfrom(200)
        print(f"Received: {data.decode()}")
    except socket.timeout:
        pass
    except socket.error as msg:
        print(msg)