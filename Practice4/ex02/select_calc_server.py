import sys
import socket
import struct
import select

server_addr = sys.argv[1]
server_port = int(sys.argv[2])
timeout = 1

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((server_addr, server_port))

    ops = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x // y,
    }

    unpacker = struct.Struct("i i 1s")

    server.listen(5)
    inputs = [server]

    while True:
        try:
            (readables, _, _)= select.select(inputs, [], [], timeout)
            for s in readables:
                if s is server:
                    connection, client_info = server.accept()
                    print(f"Someone has connected: {client_info[0]}:{client_info[1]}")
                    inputs.append(connection)
                else:
                    msg = s.recv(unpacker.size)
                    if not msg:
                        s.close()
                        print("The client has terminated the connection")
                        inputs.remove(s)
                        continue
                    operand_a, operand_b, operator = unpacker.unpack(msg)
                    operator = operator.decode()
                    print(f"The client's message: {operand_a} {operator} {operand_b}")
                    result = ops[operator](operand_a, operand_b)
                    msg = unpacker.pack(result, 0, b"R")
                    s.sendall(msg)
                    print(f"Sent response: {result}")
        except KeyboardInterrupt:
            for s in inputs:
                s.close()
            print("Server closing")
            break