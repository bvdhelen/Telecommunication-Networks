import socket
import struct
import hashlib
import random

HOST = '127.0.0.1'
PORT = 5000

def calculate_md5(data):
    return hashlib.md5(data).digest()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f"[LOTTERY SERVER] Listening on {HOST}:{PORT}")

conn, addr = server.accept()
print(f"[LOTTERY SERVER] Connected by {addr}")

# Recibimos exactamente 25 bytes
data = conn.recv(25)

if data:
    # Desempaquetamos: 16s (MD5), 5B (números), I (apuesta)
    received_hash, *rest = struct.unpack('!16s5BI', data)
    client_numbers = list(rest[:5])
    bet = rest[5]
    
    # Verificamos el MD5
    raw_data = struct.pack('!5BI', *client_numbers, bet)
    if received_hash != calculate_md5(raw_data):
        print("[LOTTERY SERVER] Invalid MD5! Data corrupted.")
        conn.sendall(b"ERROR")
    else:
        print(f"[LOTTERY SERVER] Valid data. Numbers: {client_numbers}, Bet: {bet}")
        
        # Sorteo
        draw = [random.randint(1, 20) for _ in range(5)]
        
        # Calcular ganancias (1 acierto = 1x, 2 aciertos = 2x...)
        hits = sum(1 for n in client_numbers if n in draw)
        winnings = hits * bet
        
        print(f"[LOTTERY SERVER] Draw: {draw}, Hits: {hits}, Winnings: {winnings}")
        
        # Empaquetar respuesta
        response_raw = struct.pack('!5BI', *draw, winnings)
        response_hash = calculate_md5(response_raw)
        response_packet = struct.pack('!16s', response_hash) + response_raw
        
        conn.sendall(response_packet)
        print("[LOTTERY SERVER] Response sent.")

conn.close()
server.close()
