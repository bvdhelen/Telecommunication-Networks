import socket

# Client configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
SERVER_ADDRESS = (SERVER_HOST, SERVER_PORT)

# Name of the image we are going to send
image_path = "net.jpg" 

# Create the UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    with open(image_path, "rb") as f:
        print(f"[CLIENT] Sending file '{image_path}' to {SERVER_ADDRESS}...")
        
        while True:
            # Read exactly 200 bytes
            chunk = f.read(200)
            
            if chunk:
                # Send the chunk to the server
                client_socket.sendto(chunk, SERVER_ADDRESS)
                print(f"[CLIENT] Sent chunk of {len(chunk)} bytes.")
                
                # Wait for the server's acknowledgment (ACK)
                ack, _ = client_socket.recvfrom(1024)
                if ack != b"OK":
                    print("[CLIENT] Warning: 'OK' was not received correctly.")
            else:
                # If the chunk is empty, we have reached the end of the file
                print("[CLIENT] End of file reached. Sending empty string (EOF)...")
                client_socket.sendto(b"", SERVER_ADDRESS)
                break
                
    print("[CLIENT] Transfer completed successfully.")

except FileNotFoundError:
    print(f"[ERROR] The file '{image_path}' does not exist. Make sure to put an image in the same folder.")
finally:
    client_socket.close()
