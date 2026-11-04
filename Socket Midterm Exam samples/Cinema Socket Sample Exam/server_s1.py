import socket
import struct
import random
import string

HOST = '127.0.0.1'
PORT = 12345

def generate_ticket_id():
    # Genera 6 caracteres aleatorios en mayúsculas y números
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
    # Enviar la lista (Simulada para esta subtarea)
    screenings = b"Dune;Hall 1;17:30|Oppenheimer;Hall 2;19:00|Barbie;Hall 1;20:45"
    connection.sendall(screenings)
    print(f"[SERVER] Sent screenings.")

# 2. Recibir petición de compra
data = connection.recv(1024)
print(f"[SERVER] Received purchase request: {data.decode()}")

# Simulamos que siempre hay éxito para probar el flujo (Subtask 2 arreglará esto)
result = b"SUCCESS"
ticket_id = generate_ticket_id()
print(f"[SERVER] Purchase successful! Ticket: {ticket_id.decode()}")

# 3. Empaquetar y enviar respuesta
response = struct.pack('7s6s', result, ticket_id)
connection.sendall(response)

connection.close()
server.close()
