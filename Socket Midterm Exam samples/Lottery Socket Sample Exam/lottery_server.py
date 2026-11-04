import socket
import select
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
server.setblocking(False)
inputs = [server]
print(f"[LOTTERY SERVER] Listening on {HOST}:{PORT}")

while True:
    readable, _, _ = select.select(inputs, [], [])
    
    for s in readable:
        if s is server:
            conn, addr = s.accept()
            conn.setblocking(False)
            inputs.append(conn)
            print(f"[LOTTERY SERVER] New client from {addr}")
        else:
            try:
                # Recibimos exactamente 25 bytes (16s + 5B + I)
                data = s.recv(25)
                if data:
                    # Desempaquetamos: MD5 (16s), 5 números (5B), apuesta (I)
                    received_hash, *rest = struct.unpack('!16s5BI', data)
                    client_numbers = rest[:5]
                    bet = rest[5]
                    
                    # Reconstruimos los datos SIN el hash para verificar el checksum
                    raw_data = struct.pack('!5BI', *client_numbers, bet)
                    calculated_hash = calculate_md5(raw_data)
                    
                    if received_hash != calculated_hash:
                        print(f"[LOTTERY SERVER] Invalid MD5 from {s.getpeername()}. Ignoring.")
                        s.sendall(b"ERROR")
                        continue
                    
                    print(f"[LOTTERY SERVER] Valid request. Numbers: {client_numbers}, Bet: {bet}")
                    
                    # Sorteo: 5 números aleatorios del 1 al 20
                    draw = [random.randint(1, 20) for _ in range(5)]
                    
                    # Calcular aciertos
                    hits = sum(1 for n in client_numbers if n in draw)
                    winnings = hits * bet
                    
                    print(f"[LOTTERY SERVER] Draw: {draw}, Hits: {hits}, Winnings: {winnings}")
                    
                    # Empaquetar respuesta
                    response_raw = struct.pack('!5BI', *draw, winnings)
                    response_hash = calculate_md5(response_raw)
                    response_packet = struct.pack('!16s', response_hash) + response_raw
                    
                    s.sendall(response_packet)
                    print(f"[LOTTERY SERVER] Response sent.")
                    
                else:
                    inputs.remove(s)
                    s.close()
            except Exception as e:
                inputs.remove(s)
                s.close()
