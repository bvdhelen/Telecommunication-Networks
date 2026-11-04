import socket
import sys
import json
import datetime

if len(sys.argv) != 4:
    print("Usage: python logger_server.py <ip> <port> <log.json>")
    sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])
LOG_FILE = sys.argv[3]

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))
print(f"[LOGGER] Listening on UDP {HOST}:{PORT}")

while True:
    data, addr = server.recvfrom(1024)
    msg = data.decode()
    print(f"[LOGGER] Received: {msg}")
    
    try:
        # Formato: timestamp|student_ip|item_id|quantity|total_price
        timestamp, student_ip, item_id, quantity, total_price = msg.split('|')
        
        log_entry = {
            "timestamp": timestamp,
            "student_ip": student_ip,
            "item_id": item_id,
            "quantity": int(quantity),
            "total_price": int(total_price)
        }
        
        # Leer JSON actual
        try:
            with open(LOG_FILE, 'r') as f:
                logs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []
            
        # Añadir y guardar
        logs.append(log_entry)
        with open(LOG_FILE, 'w') as f:
            json.dump(logs, f, indent=4)
            
        print(f"[LOGGER] Order logged to {LOG_FILE}")
    except Exception as e:
        print(f"[LOGGER] Error parsing message: {e}")
        
    # Enviar ACK
    server.sendto(b"ACK", addr)
    print(f"[LOGGER] ACK sent to {addr}")
