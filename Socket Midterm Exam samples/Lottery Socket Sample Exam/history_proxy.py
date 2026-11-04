import socket
import struct
import json
import datetime

# Configuración
PROXY_PORT = 6000        # Escucha al cliente por UDP
LOTTERY_HOST = '127.0.0.1'
LOTTERY_PORT = 5000      # Habla con el servidor por TCP
LOG_FILE = 'lottery_log.json'

udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind(('127.0.0.1', PROXY_PORT))
print(f"[HISTORY PROXY] Listening on UDP {PROXY_PORT}")

while True:
    # 1. Recibir del cliente (UDP)
    data, client_addr = udp_server.recvfrom(1024)
    print(f"[HISTORY PROXY] Received data from {client_addr}")
    
    # 2. Conectar al Lottery Server (TCP)
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client.connect((LOTTERY_HOST, LOTTERY_PORT))
    
    # 3. Reenviar (Proxy)
    tcp_client.sendall(data)
    
    # 4. Recibir respuesta del servidor
    response = tcp_client.recv(1024)
    tcp_client.close()
    
    # 5. Loguear en JSON (Task V)
    try:
        # Desempaquetamos para saber qué números eligió y qué ganó
        _, *rest = struct.unpack('!16s5BI', data)
        client_numbers, bet = rest[:5], rest[5]
        
        _, *rest_resp = struct.unpack('!16s5BI', response)
        draw, winnings = rest_resp[:5], rest_resp[5]
        
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "client_ip": client_addr[0],
            "picked_numbers": client_numbers,
            "bet": bet,
            "drawn_numbers": draw,
            "winnings": winnings
        }
        
        # Append al JSON
        try:
            with open(LOG_FILE, 'r') as f:
                logs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []
            
        logs.append(log_entry)
        with open(LOG_FILE, 'w') as f:
            json.dump(logs, f, indent=4)
            
        print(f"[HISTORY PROXY] Logged to {LOG_FILE}")
    except Exception as e:
        print(f"[HISTORY PROXY] Error logging: {e}")

    # 6. Devolver respuesta al cliente (UDP)
    udp_server.sendto(response, client_addr)
    print(f"[HISTORY PROXY] Result forwarded to client.")
