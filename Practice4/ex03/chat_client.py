import socket
import threading

# Configuration
HOST = '127.0.0.1'  # Localhost address
PORT = 5555         # Listening port

# Dictionary to store connected clients {socket: name}
clients = {}

def broadcast_message(message, sender_socket):
    """Sends the message to all clients except the one who sent it."""
    for client in list(clients.keys()):
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                # If there's an error, remove the client
                client.close()
                if client in clients:
                    del clients[client]

def handle_client(client_socket):
    """Function that runs in a thread for each connected client."""
    try:
        # 1. The first thing the client does is send their name
        name = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = name
        print(f"[NEW CONNECTION] {name} has joined the chat.")
        
        # Notify others that someone joined (optional, but good practice)
        welcome_message = f"[SYSTEM] {name} has joined the chat.".encode('utf-8')
        broadcast_message(welcome_message, client_socket)

        # 2. Loop to receive messages from this client
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break # If the message is empty, the client disconnected
            
            # 3. Format the message: [<name>] message
            formatted_message = f"[{name}] {message}"
            print(formatted_message) # Print to server console (optional)
            
            # 4. Forward to others
            broadcast_message(formatted_message, client_socket)

    except Exception as e:
        print(f"Error with client: {e}")
    finally:
        # Cleanup when the client disconnects
        if client_socket in clients:
            name = clients[client_socket]
            print(f"[DISCONNECTION] {name} has left.")
            del clients[client_socket]
            client_socket.close()

# --- SERVER START ---
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print(f"Server is listening on {HOST}:{PORT}...")

while True:
    # Accept new connections
    client_socket, address = server.accept()
    # Create a thread to handle the client
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()
