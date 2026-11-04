import socket
import select
import struct
import hashlib
import random
import sys

# --- CONFIGURACIÓN BÁSICA ---
HOST = '127.0.0.1'
PORT = 5000

# Función auxiliar para calcular el hash MD5 de los datos
def calculate_md5(data):
    return hashlib.md5(data).digest()

# --- CREACIÓN DEL SOCKET SERVIDOR ---
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Permite reutilizar el puerto inmediatamente si el servidor se reinicia rápido
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
server.bind((HOST, PORT))
server.listen(5) # Cola de espera para hasta 5 conexiones pendientes

# ¡VITAL PARA SELECT! Ponemos el socket en modo no bloqueante.
# Esto significa que accept() o recv() no se quedarán colgados esperando si no hay datos.
server.setblocking(False) 

# Lista de sockets que 'select' va a vigilar constantemente
inputs = [server]
print(f"[LOTTERY SERVER] Listening on {HOST}:{PORT} (Select mode enabled)")

# --- BUCLE PRINCIPAL ---
while True:
    # select() bloquea el programa hasta que haya actividad en algún socket de 'inputs'.
    # 'readable' será una lista de los sockets que tienen datos listos para leer.
    readable, _, _ = select.select(inputs, [], [])
    
    # Iteramos sobre los sockets que tienen actividad
    for s in readable:
        
        # CASO 1: El socket con actividad es el servidor principal.
        # Esto significa que un nuevo cliente quiere conectarse.
        if s is server:
            try:
                conn, addr = s.accept()
                conn.setblocking(False) # Modo no bloqueante para el nuevo cliente
                inputs.append(conn)     # Añadimos al cliente a la lista de vigilancia de select
                print(f"[LOTTERY SERVER] New client connected from {addr}")
            except Exception as e:
                print(f"[ERROR] Accept failed: {e}")
                
        # CASO 2: El socket con actividad es un cliente ya conectado.
        # Esto significa que el cliente ha enviado datos (su apuesta).
        else:
            try:
                # Recibimos exactamente los 25 bytes de nuestro struct
                data = s.recv(25)
                
                if data:
                    print(f"[LOTTERY SERVER] Received data from {s.getpeername()}")
                    
                    # --- DESEMPAQUETADO Y VERIFICACIÓN MD5 ---
                    # '!16s5BI' significa: 16 bytes string (hash), 5 bytes sin signo (números), 1 entero sin signo (apuesta)
                    received_hash, *rest = struct.unpack('!16s5BI', data)
                    client_numbers = list(rest[:5])
                    bet = rest[5]
                    
                    # Reconstruimos los datos SIN el hash para comprobar integridad
                    raw_data = struct.pack('!5BI', *client_numbers, bet)
                    
                    if received_hash != calculate_md5(raw_data):
                        print("[LOTTERY SERVER] Invalid MD5! Data corrupted. Ignoring.")
                        s.sendall(b"ERROR")
                    else:
                        # --- LÓGICA DEL SORTEO ---
                        print(f"[LOTTERY SERVER] Valid data. Client numbers: {client_numbers}, Bet: {bet}")
                        
                        # Generamos 5 números aleatorios del 1 al 20
                        draw = [random.randint(1, 20) for _ in range(5)]
                        
                        # Calculamos cuántos números ha acertado el cliente
                        hits = sum(1 for n in client_numbers if n in draw)
                        winnings = hits * bet
                        
                        print(f"[LOTTERY SERVER] Draw: {draw}, Hits: {hits}, Winnings: {winnings}")
                        
                        # --- EMPAQUETAR Y ENVIAR RESPUESTA ---
                        # Empaquetamos los números sorteados y las ganancias
                        response_raw = struct.pack('!5BI', *draw, winnings)
                        # Calculamos el MD5 de la respuesta para que el cliente verifique
                        response_hash = calculate_md5(response_raw)
                        # Unimos el hash + los datos
                        response_packet = struct.pack('!16s', response_hash) + response_raw
                        
                        s.sendall(response_packet)
                        print(f"[LOTTERY SERVER] Response sent to {s.getpeername()}")
                
                # Si data está vacío (b''), el cliente ha cerrado la conexión
                else:
                    print(f"[LOTTERY SERVER] Client disconnected.")
                    # Lo quitamos de la lista de vigilancia y cerramos el socket
                    inputs.remove(s)
                    s.close()
                    
            except ConnectionResetError:
                # Manejo de errores por si el cliente se desconecta abruptamente
                print(f"[LOTTERY SERVER] Client reset connection.")
                inputs.remove(s)
                s.close()
