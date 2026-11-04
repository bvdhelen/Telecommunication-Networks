import socket

# Server configuration
HOST = '127.0.0.1'
PORT = 12345
BUFFER_SIZE = 1024 # Buffer size (must be larger than 200)

# Create the UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"[SERVER] Listening on {HOST}: {PORT}...")

# File where we will save the received picture
file_name = "received_image.jpg"
with open(file_name, "wb") as f:
    while True:
        # Receive the chunk and the client's address
        data, client_address = server_socket.recvfrom(BUFFER_SIZE)
        
        # If we receive an empty string, it means the file has ended
        if data == b"":
            print("[SERVER] End of file received (EOF).")
            break
        
        # Write the received data to the file
        f.write(data)
        print(f"[SERVER] Received {len(data)} bytes from {client_address}")
        
        # Acknowledge the reception to the client
        server_socket.sendto(b"OK", client_address)

print(f"[SERVER] File saved as '{file_name}'.")
server_socket.close()
