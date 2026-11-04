import sys
import socket
import struct
import select

proxy_addr = sys.argv[1]
proxy_port = int(sys.argv[2])
server_addr = sys.argv[3]
server_port = int(sys.argv[4])

packer = struct.Struct("i i c")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as proxy: #IPv4, UDP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server: #IPv4, TCP
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.settimeout(1)
        server.bind((proxy_addr, proxy_port))

        server.listen(5)

        inputs = [server]

        while True:
            try:
                readables, _, _ = select.select(inputs, [], [])
                for s in readables:
                    if s is server:
                        connection, client_info = server.accept()
                        print(f"Someone has connected: {client_info[0]}: {client_info[1]}")
                        inputs.append(connection)
                    else:
                        msg = s.recv(packer.size)
                        if not msg:
                            s.close()
                            print("The client has terminated the connection")
                            inputs.remove(s)
                            continue
                        parsed_msg = packer.unpack(msg)
                        print(f"The client's message: {parsed_msg[0]} {parsed_msg[2].decode()} {parsed_msg[1]}")
                        proxy.sendto(msg, (server_addr, server_port))
                        result, _ = proxy.recvfrom(packer.size)
                        parsed_msg = packer.unpack(result)
                        print(f"The server's response: {parsed_msg[0]} {parsed_msg[2].decode()} {parsed_msg[1]}")
                        s.sendall(result)

            except socket.timeout:
                pass
            except KeyboardInterrupt:
                print("Proxy sutting down")
                proxy.close()
                server.close()
                break
