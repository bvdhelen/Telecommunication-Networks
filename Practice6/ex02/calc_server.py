import sys
import socket
import struct
import select

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((server_addr, server_port))

sock.listen(5)

ops = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x // y,
}

packer = struct.Struct("i i 1s")

inputs = [sock]
timeout = 1.0

while True:
    try:
        readables, _, _ = select.select(inputs, [], [], timeout)

        for s in readables:
            if s is sock:
                connection, client_info = sock.accept()
                print(f"Someone has connected: {client_info[0]}:{client_info[1]}")
                inputs.append(connection)
            else:
                msg = s.recv(packer.size)
                if not msg:
                    s.close()
                    print("The client has terminated the connection")
                    inputs.remove(s)
                    continue
                operand_a, operand_b, operator = packer.unpack(msg)
                operator = operator.decode()
                print(f"The client's message: {operand_a} {operator} {operand_b}")
                result = ops[operator](operand_a, operand_b)
                msg = packer.pack(result, 0, b"R")
                s.sendall(msg)
                print(f"Sent response: {result}")

    except KeyboardInterrupt:
        for s in inputs:
            s.close()
        print("Server closing")
        break