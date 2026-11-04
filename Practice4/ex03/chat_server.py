import socket
import select

HOST = '127.0.0.1'
PORT = 5555

# Create the socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Prevents the "Address already in use" error
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
print(f"Server listening on {HOST}:{PORT}...")

# List of sockets we are going to "watch" (starts with the server)
sockets_list = [server]
# Dictionary to store names: {client_socket: "name"}
clients = {}

# Helper function to remove a client and notify the others
def remove_client(client_socket):
    if client_socket in clients:
        name = clients[client_socket]
        print(f"[DISCONNECTION] {name} has left the chat.")
        
        # Notify the OTHER clients that this person left
        leave_msg = f"[SYSTEM] {name} has left the chat."
        for c in clients:
            if c != client_socket:
                try:
                    c.send(leave_msg.encode('utf-8'))
                except:
                    pass
        
        del clients[client_socket]
    
    if client_socket in sockets_list:
        sockets_list.remove(client_socket)
    try:
        client_socket.close()
    except:
        pass

while True:
    # select tells us which sockets are ready to be read
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        # Case 1: The server has a new connection
        if notified_socket == server:
            client_socket, client_address = server.accept()
            sockets_list.append(client_socket)
            print(f"[NEW CONNECTION] from {client_address}")
        
        # Case 2: A client has sent a message (or disconnected)
        else:
            try:
                message = notified_socket.recv(1024).decode('utf-8')
                
                # If the message is empty, the client disconnected
                if not message:
                    remove_client(notified_socket)
                    continue

                # If the client does NOT have a name yet, this message is their name
                if notified_socket not in clients:
                    clients[notified_socket] = message
                    print(f"[NEW USER] Name: {message}")
                    
                    # Notify the OTHER clients that this person joined
                    join_msg = f"[SYSTEM] {message} has joined the chat."
                    for client_socket in clients:
                        if client_socket != notified_socket:
                            try:
                                client_socket.send(join_msg.encode('utf-8'))
                            except:
                                pass
                
                # If they already have a name, it's a normal chat message
                else:
                    name = clients[notified_socket]
                    formatted_message = f"[{name}] {message}"
                    print(formatted_message)
                    
                    # Forward to all other clients
                    for client_socket in clients:
                        if client_socket != notified_socket:
                            try:
                                client_socket.send(formatted_message.encode('utf-8'))
                            except:
                                pass
            except:
                # If a socket errors out (e.g. connection reset by peer), remove it cleanly
                remove_client(notified_socket)
