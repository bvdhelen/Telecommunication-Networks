import socket
import struct
import random
import string
import sys

# Verificamos que se pasó el archivo
if len(sys.argv) != 2:
    print("Usage: python server_s2.py <screenings_file.txt>")
    sys.exit(1)

file_path = sys.argv[1]
screenings_data = {} # Diccionario: {"Pelicula;Hora": asientos}
screenings_string_parts = []

# Leer archivo
try:
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            title, hall, time, seats = line.split(';')
            key = f"{title};{time}"
            screenings_data[key] = int(seats)
            screenings_string_parts.append(f"{title};{hall};{time}")
except FileNotFoundError:
    print("File not found!")
    sys.exit(1)

# Aquí preparamos la respuesta con los datos REALES del archivo
screenings_response = "|".join(screenings_string_parts).encode()

HOST = '127.0.0.1'
PORT = 12345

def generate_ticket_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)).encode()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f"[SERVER] Listening on {HOST}: {PORT}")

connection, addr = server.accept()
print(f"[SERVER] Connected by {addr}")

# 1. Recibir GET_SCREENINGS
data = connection.recv(1024)
print(f"[SERVER] Received: {data.decode()}")

if data == b"GET_SCREENINGS":
    # Enviar la lista leída del archivo
    connection.sendall(screenings_response)
    print(f"[SERVER] Sent screenings from file.")

# 2. Recibir petición de compra
data = connection.recv(1024)
request_str = data.decode()
print(f"[SERVER] Received purchase request: {request_str}")

# 3. Lógica de compra
# Comprobar si la película existe en el diccionario y si tiene asientos > 0
if request_str in screenings_data and screenings_data[request_str] > 0:
    # Hay asientos, descontamos 1
    screenings_data[request_str] -= 1
    result = b"SUCCESS"
    ticket_id = generate_ticket_id()
    print(f"[SERVER] Purchase successful! Ticket: {ticket_id.decode()}. Seats left: {screenings_data[request_str]}")
else:
    # No hay asientos o la película no existe
    result = b"FAIL"
    ticket_id = b"000000"
    print(f"[SERVER] Purchase failed. No seats available or invalid screening.")

# 4. Empaquetar y enviar respuesta
response = struct.pack('7s6s', result, ticket_id)
connection.sendall(response)

connection.close()
server.close()
