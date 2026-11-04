import socket
import sys

if len(sys.argv) != 3:
    print("Usage: python student_client_f1.py <ip> <port>")
    sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    action = input("\nEnter action (VIEW/ORDER/QUIT): ").strip().upper()
    
    if action == "QUIT":
        print("Disconnecting...")
        break
        
    item_id = input("Enter item ID: ").strip().upper()
    qty_str = input("Enter quantity (or 0 for VIEW): ").strip()
    
    # Construimos el mensaje
    msg = f"{action}|{item_id}|{qty_str}"
    print(f"Sent: {msg}")
    
    client.sendall(msg.encode())
    
    # Recibimos respuesta
    response = client.recv(1024).decode()
    print(f"Response: {response}")

client.close()
