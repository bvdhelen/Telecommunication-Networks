import socket
import sys
import json
import select

# ... (La carga del menú es igual que en F1) ...
if len(sys.argv) < 3:
    sys.exit(1)
HOST = sys.argv[1]
PORT = int(sys.argv[2])

with open('menu.json', 'r') as f:
    menu = {item['item_id']: item for item in json.load(f)}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)
server.setblocking(False)

inputs = [server]
print(f"[SERVER] Listening on {HOST}:{PORT} (Select mode)")

while True:
    readable, _, _ = select.select(inputs, [], [])
    
    for s in readable:
        if s is server:
            # Nuevo cliente
            conn, addr = s.accept()
            conn.setblocking(False)
            inputs.append(conn)
            print(f"[SERVER] New connection from {addr}")
        else:
            # Datos de un cliente
            try:
                data = s.recv(1024)
                if data:
                    msg = data.decode().strip()
                    print(f"[SERVER] Received from {s.getpeername()}: {msg}")
                    
                    # ... (La lógica de validación y negocio es EXACTAMENTE la misma que en F1) ...
                    # Copia y pega el bloque de validación desde F1 aquí.
                    # En lugar de conn.sendall(), usa s.sendall()
                    
                    # Ejemplo simplificado de la lógica:
                    parts = msg.split('|')
                    response = "ERROR" # Por defecto
                    
                    if len(parts) == 3:
                        action, item_id, quantity_str = parts
                        if action in ["VIEW", "ORDER"] and len(item_id) == 4 and item_id.isupper() and quantity_str.isdigit():
                            quantity = int(quantity_str)
                            if (action == "VIEW" and quantity == 0) or (action == "ORDER" and quantity > 0):
                                if item_id in menu:
                                    item = menu[item_id]
                                    if action == "VIEW":
                                        response = f"{item['name']}:{item['price']}:{item['stock']}"
                                    else:
                                        if item['stock'] >= quantity:
                                            item['stock'] -= quantity
                                            response = f"SUCCESS:{item['price'] * quantity}"
                                        else:
                                            response = "NO_STOCK"
                                else:
                                    response = "NOT_FOUND"
                    
                    s.sendall(response.encode())
                    print(f"[SERVER] Sending to {s.getpeername()}: {response}")
                else:
                    print(f"[SERVER] Client disconnected.")
                    inputs.remove(s)
                    s.close()
            except ConnectionResetError:
                inputs.remove(s)
                s.close()
