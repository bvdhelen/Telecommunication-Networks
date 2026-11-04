import socket
import struct
import random

PROXY_PORT = 12346
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

# Configuración del Proxy (actúa como servidor para el cliente)
proxy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_server.bind(('127.0.0.1', PROXY_PORT))
proxy_server.listen(5)
print(f"[PROXY] Listening on port {PROXY_PORT}...")

while True:
    # 1. Aceptar conexión del Cliente
    client_conn, client_addr = proxy_server.accept()
    print(f"\n[PROXY] Client connected.")
    
    # 2. Conectar al Servidor Real
    server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_conn.connect((SERVER_HOST, SERVER_PORT))
    
    # --- FASE 1: Retransmitir GET_SCREENINGS ---
    request_screenings = client_conn.recv(1024)
    server_conn.sendall(request_screenings)
    
    response_screenings = server_conn.recv(1024)
    client_conn.sendall(response_screenings)
    print("[PROXY] Relayed screenings.")
    
    # --- FASE 2: Retransmitir la Compra ---
    request_buy = client_conn.recv(1024)
    server_conn.sendall(request_buy)
    print(f"[PROXY] Relayed purchase request: {request_buy.decode()}")
    
    # --- FASE 3: Interceptar la Respuesta ---
    response_buy = server_conn.recv(1024)
    
    # Desempaquetamos el struct (7s6s)
    result, ticket_id = struct.unpack('7s6s', response_buy)
    result_str = result.decode().strip('\x00')
    ticket_str = ticket_id.decode().strip('\x00')
    
    if result_str == "SUCCESS":
        # Lanzamos la moneda al aire (50% de probabilidad)
        if random.random() < 0.5:
            # Caras: Reenviamos el ticket legítimo
            print(f"[PROXY] Forwarded ticket: {ticket_str}")
            client_conn.sendall(response_buy)
        else:
            # Cruces: ¡Robamos el ticket!
            print(f"[PROXY] Stolen ticket: {ticket_str}")
            # Creamos un falso FAIL, 000000 usando struct
            fake_response = struct.pack('7s6s', b"FAIL", b"000000")
            client_conn.sendall(fake_response)
    else:
        # Si el servidor ya había dicho FAIL, lo reenviamos tal cual
        print(f"[PROXY] Forwarded failed purchase: FAIL, 000000")
        client_conn.sendall(response_buy)

    # Cerramos las conexiones de este cliente para pasar al siguiente
    client_conn.close()
    server_conn.close()
