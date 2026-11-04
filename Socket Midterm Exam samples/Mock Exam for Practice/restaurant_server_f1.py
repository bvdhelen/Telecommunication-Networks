import socket
import sys
import json

# --- CARGAR EL MENÚ DESDE JSON (Task 2) ---
if len(sys.argv) < 3:
    print("Usage: python restaurant_server_f1.py <ip> <port>")
    sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])
MENU_FILE = 'menu.json' # Hardcodeado temporalmente para la Fase 1

try:
    with open(MENU_FILE, 'r') as f:
        menu_list = json.load(f)
        # Convertimos la lista a un diccionario para búsquedas rápidas por item_id
        menu = {item['item_id']: item for item in menu_list}
    print(f"[SERVER] Menu loaded from {MENU_FILE}:")
    for k, v in menu.items():
        print(f"  {k}: {v['name']} - ${v['price']/100:.2f} (Stock: {v['stock']})")
except Exception as e:
    print(f"[ERROR] Could not load menu: {e}")
    sys.exit(1)

# --- CONFIGURACIÓN DEL SOCKET ---
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)
print(f"\n[SERVER] Listening on {HOST}:{PORT}")

conn, addr = server.accept()
print(f"[SERVER] Connected by {addr}")

while True:
    # Recibimos datos
    data = conn.recv(1024)
    if not data:
        print("[SERVER] Client disconnected.")
        break
        
    msg = data.decode().strip()
    print(f"[SERVER] Received: {msg}")
    
    # --- VALIDACIÓN ESTRICTA (Task 1) ---
    parts = msg.split('|')
    
    # 1. Debe tener exactamente 3 partes
    if len(parts) != 3:
        response = "ERROR"
    else:
        action, item_id, quantity_str = parts
        
        # 2. Validar acción, item_id y cantidad (entero)
        if action not in ["VIEW", "ORDER"]:
            response = "ERROR"
        elif len(item_id) != 4 or not item_id.isalpha() or not item_id.isupper():
            response = "ERROR"
        elif not quantity_str.isdigit():
            response = "ERROR"
        else:
            quantity = int(quantity_str)
            
            # 3. Validaciones específicas por acción
            if action == "VIEW" and quantity != 0:
                response = "ERROR"
            elif action == "ORDER" and quantity <= 0:
                response = "ERROR"
            else:
                # --- LÓGICA DE NEGOCIO ---
                if item_id not in menu:
                    response = "NOT_FOUND"
                else:
                    item = menu[item_id]
                    
                    if action == "VIEW":
                        response = f"{item['name']}:{item['price']}:{item['stock']}"
                    
                    elif action == "ORDER":
                        if item['stock'] < quantity:
                            response = "NO_STOCK"
                        else:
                            # Éxito: descontar stock y calcular total
                            item['stock'] -= quantity
                            total_price = item['price'] * quantity
                            response = f"SUCCESS:{total_price}"
                            print(f"[SERVER] Stock updated. {item_id} now has {item['stock']} left.")
                            
    # Enviar respuesta
    conn.sendall(response.encode())
    print(f"[SERVER] Sending: {response}")

conn.close()
server.close()
