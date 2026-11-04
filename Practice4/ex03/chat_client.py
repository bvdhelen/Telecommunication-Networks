import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 5555

# 1. Connect and send name
name = input("Enter your name: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.send(name.encode('utf-8'))

# 2. This function runs in the background to print incoming messages
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                break
            print(message) # Print to standard output
        except:
            break
    
    # If the loop breaks, connection is dead. Kill the program instantly.
    os._exit(0) 

# Start the background thread
threading.Thread(target=receive_messages, daemon=True).start()

# 3. Main loop: just wait for you to type and send
try:
    while True:
        text = input("") # Waits for you to press Enter
        client.send(text.encode('utf-8'))
except (KeyboardInterrupt, EOFError):
    os._exit(0) # Clean exit when you press Ctrl+C
