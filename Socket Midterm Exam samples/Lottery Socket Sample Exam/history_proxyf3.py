import socket
import struct
import json
import datetime

# --- CONFIGURACIÓN ---
PROXY_PORT = 6000          # Puerto UDP donde escucha el cliente
LOTTERY_HOST = '127.0.0.1' # IP del servidor real (TCP)
LOTTERY_PORT = 5000        # Puerto del servidor real
LOG_FILE = 'lottery_log.json' # Archivo donde se guardará el historial

# --- SOCKET UDP (Para hablar con el Cliente) ---
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind(('127.0.0.1', PROXY_PORT))
print(f"[HISTORY PROXY] Listening on UDP port {PROXY_PORT}")

while True:
    # 1. Recibimos los 25 bytes del cliente por UDP
    data, client_addr = udp_server.recvfrom(1024)
    print(f"\n[HISTORY PROXY] Received {len(data)} bytes from {client_addr}")
    
    # --- SOCKET TCP (Para hablar con el Lottery Server) ---
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client.connect((LOTTERY_HOST, LOTTERY_PORT))
    
    # 2. Reenviamos los datos EXACTOS al servidor de la lotería
    tcp_client.sendall(data)
    
    # 3. Recibimos la respuesta del servidor de la lotería
    response = tcp_client.recv(25)
    tcp_client.close()
    
    # 4. Logueamos en el archivo JSON
    try:
        # Desempaquetamos la petición del cliente para saber qué números eligió
        _, *req_rest = struct.unpack('!16s5BI', data)
        picked_numbers = list(req_rest[:5])
        bet = req_rest[5]
        
        # Desempaquetamos la respuesta del servidor para saber qué salió
        _, *resp_rest = struct.unpack('!16s5BI', response)
        drawn_numbers = list(resp_rest[:5])
        winnings = resp_rest[5]
        
        # Creamos la entrada del log
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "client_address": f"{client_addr[0]}:{client_addr[1]}",
            "picked_numbers": picked_numbers,
            "bet": bet,
            "drawn_numbers": drawn_numbers,
            "winnings": winnings
        }
        
        # Leemos el JSON actual (o creamos una lista vacía si no existe)
        try:
            with open(LOG_FILE, 'r') as f:
                logs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []
            
        # Añadimos el nuevo log y guardamos (Append)
        logs.append(log_entry)
        with open(LOG_FILE, 'w') as f:
            json.dump(logs, f, indent=4)
            
        print(f"[HISTORY PROXY] Logged game to {LOG_FILE}")
        
    except Exception as e:
        print(f"[HISTORY PROXY] Error while logging: {e}")

    # 5. Devolvemos la respuesta al cliente por UDP
    udp_server.sendto(response, client_addr)
    print(f"[HISTORY PROXY] Forwarded result back to {client_addr}")
