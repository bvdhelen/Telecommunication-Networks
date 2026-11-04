import socket
import sys
import select

TCP_IP = "localhost" # "127.0.0.1"
TCP_PORT = int(sys.argv[1])
BUFFER_SIZE = 1024
REPLY = "Hello client".encode()
TIMEOUT = 1

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #to reuse this addr
    sock.bind((TCP_IP, TCP_PORT))
    sock.listen(5)

    inputs = [sock]

    while True:
        try:
            (readables, _, _) = select.select(inputs, [], [], TIMEOUT)

            for s in readables:
                if s is sock:
                    connection, client_info = sock.accept()
                    print(f"Someone has connected: {client_info[0]}:{client_info[1]}")
                    inputs.append(connection)
                else:
                    msg = s.recv(BUFFER_SIZE)
                    if not msg:
                        s.close()
                        print("The client has terminated the connection")
                        inputs.remove(s)
                        continue
                    print("The client's message:", msg.decode())
                    s.sendall(REPLY)
                    print("Sent response:", REPLY)


        except KeyboardInterrupt:
            for s in inputs:
                s.close()
            print("Server closing")
            break