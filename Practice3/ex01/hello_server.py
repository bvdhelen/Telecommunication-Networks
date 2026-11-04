import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4, TCP

#server_addr = ("", 10000) #("localhost", 10000) <- only accepts conexions with the local host
server_addr = ("localhost", int(sys.argv[1]))

sock.bind(server_addr)
sock.listen(1)
sock.settimeout(1)

while True:
    try:
        print("Waiting...")
        client_socket, client_addr = sock.accept()
        
        print("Client has connected:", client_addr)

        data = client_socket.recv(16)
        print("Received:", data.decode())
        if data:
            client_socket.sendall("Hello Client!".encode())
        else:
            print("Disconnected")
        
        client_socket.close()
    except socket.timeout:
        pass
    except KeyboardInterrupt:
        sock.close()
        break
