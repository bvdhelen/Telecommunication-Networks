#Elena Sol Díaz Contreras
#Assignment3 - Question, Answer

import socket
import select
import struct
import random
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: py server.py <bind_address> <bind_port>")
        sys.exit(1)
    
    host = sys.argv[1]
    port = int(sys.argv[2])

    # Create TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}: {port}")

    # Initial game state
    target_number = random.randint(1, 100)
    game_over = False
    inputs = [server_socket]
    print(f"Secret number chosen: {target_number}")

    try:
        while True:
            # select tells us which sockets are ready for reading
            readable, _, exceptional = select.select(inputs, [], inputs, 1.0)

            for s in readable:
                # 1. Handle New Connections
                if s is server_socket:
                    client_socket, client_address = s.accept()
                    inputs.append(client_socket)
                    print(f"New connection from {client_address}")
                # 2. Handle Messages from existing Clients
                else:
                    try:
                        data = s.recv(1024)
                        if data:
                            # Unpack the message: 1 char 'c', 1 int 'i'
                            op, num = struct.unpack('ci', data)

                            # If the game is already over, ignore the question and send 'V' (End)
                            if game_over:
                                s.sendall(struct.pack('ci', b'V', 0))
                            # If the game is still active, evaluate the question
                            else:
                                # The client asks if the number is SMALLER
                                if op == b'<':
                                    if target_number < num:
                                        s.sendall(struct.pack('ci', b'I', 0)) # Yes
                                    else:
                                        s.sendall(struct.pack('ci', b'N', 0)) # No
                                # The client asks if the number is GREATER
                                elif op == b'>':
                                    if target_number > num:
                                        s.sendall(struct.pack('ci', b'I', 0)) # Yes
                                    else:
                                        s.sendall(struct.pack('ci', b'N', 0)) # No
                                # The client tries to GUESS the exact number
                                elif op == b'=':
                                    if target_number == num:
                                        s.sendall(struct.pack('ci', b'Y', 0)) # Win
                                        game_over = True
                                        print("A client has won! Game over.")
                                    else:
                                        s.sendall(struct.pack('ci', b'K', 0)) # You are out (Lose)
                        # If recv returns empty data, the client disconnected
                        else:
                            print("Client disconnected.")
                            inputs.remove(s)
                            s.close()
                    except Exception as e:
                        print(f"Error with a client: {e}")
                        if s in inputs:
                            inputs.remove(s)
                        s.close()
            # Restart the game ONLY if it has ended and all clients have left
            if game_over and len(inputs) == 1:
                target_number = random.randint(1, 100)
                game_over = False
                print("All clients have left. New game started.")
                print(f"Secret number chosen: {target_number}")

    
    except KeyboardInterrupt:
        # Handle Ctrl+C and exit the program cleanly
        #print("\n[DEBUG] Server shutting down (Ctrl+C pressed)...")
        # Close all active sockets (server and clients)
        for sock in inputs:
            sock.close()
        print("Server closed successfully.")
        sys.exit(0)

if __name__ == "__main__":
    main()

# Submission:
    # Send it to the TMS in .zip file which should contain a client.py and a server.py only!
