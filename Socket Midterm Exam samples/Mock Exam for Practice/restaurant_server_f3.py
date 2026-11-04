import socket
import sys
import json
import select
import datetime

if len(sys.argv) != 6:
    print("Usage: python restaurant_server_f3.py <ip> <port> <menu.json> <logger_ip> <logger_port>")
    sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])
MENU_FILE = sys.argv[3]
LOGGER_IP = sys.argv[4]
LOGGER_PORT = int(sys.argv[5])
LOGGER_ADDR = (LOGGER_IP, LOGGER_PORT)

with open(MENU_FILE, 'r') as f:
    menu = {item['item_id']: item for item in json.load(f)}

# ... (Socket TCP con select igual que en F2) ...
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)
server.setblocking(False)
inputs = [server]

# Socket UDP para hablar con el Logger
udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_client.settimeout(1.0) # Esperar máximo 1 segundo el ACK

print(f"[SERVER] Listening on {HOST}:{PORT} (Select mode). Logger at {LOGGER_ADDR}")

while True:
    readable, _, _ = select.select(inputs, [], [])
    for s in readable:
        if s is server:
            conn, addr = s.accept()
            conn.setblocking(False)
            inputs.append(conn)
        else:
            try:
                data = s.recv(1024)
                if data:
                    msg = data.decode().strip()
                    parts = msg.split('|')
                    response = "ERROR"
                    
                    # Lógica de validación (igual que antes)
                    if len(parts) == 3:
                        action, item_id, quantity_str = parts
                        if action in ["VIEW", "ORDER"] and len(item_id) == 4 and item_id.isupper() and quantity_str.isdigit():
                            quantity = int(quantity_str)
                            if (action == "VIEW" and quantity == 0) or (action == "ORDER" and quantity > 0):
                                if item_id in menu:
                                    item = menu[item_id]
                                    if action == "VIEW":
                                        response = f"{item['name']}:{item['price']}:{item['stock']}"
                                    else: # ORDER
                                        if item['stock'] >= quantity:
                                            item['stock'] -= quantity
                                            total = item['price'] * quantity
                                            response = f"SUCCESS:{total}"
                                            
                                            # --- ENVIAR AL LOGGER UDP (Task 4) ---
                                            timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                                            student_ip = s.getpeername()[0]
                                            log_msg = f"{timestamp}|{student_ip}|{item_id}|{quantity}|{total}"
                                            
                                            print(f"[SERVER] Notifying Logger: {log_msg}")
                                            udp_client.sendto(log_msg.encode(), LOGGER_ADDR)
                                            
                                            try:
                                                ack, _ = udp_client.recvfrom(1024)
                                                if ack == b"ACK":
                                                    print("[SERVER] Logger ACK received.")
                                            except socket.timeout:
                                                print("[SERVER] Logger ACK timeout (ignoring).")
                                                
                                        else:
                                            response = "NO_STOCK"
                                else:
                                    response = "NOT_FOUND"
                    
                    s.sendall(response.encode())
                    print(f"[SERVER] Sent: {response}")
                else:
                    inputs.remove(s)
                    s.close()
            except ConnectionResetError:
                inputs.remove(s)
                s.close()
