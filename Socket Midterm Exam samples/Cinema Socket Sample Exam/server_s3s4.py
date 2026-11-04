import socket
import struct
import random
import string
import sys
import select

# Verificamos que se pasó el archivo
if len(sys.argv) != 2:
    print("Usage: python server_s2.py <screenings_file.txt>")
    sys.exit(1)

file_path = sys.argv[1]
screenings_data = {}
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

screenings_response = "|".join(screenings_string_parts).encode()

HOST = '127.0.0.1'
PORT = 12345

def generate_ticket_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)).encode()

# Configuración del servidor con select
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
# Es importante poner el sockete en modo no bloqueante para usar select
server.setblocking(False)

# Lista de sockets que select va a vigilar
inputs = [server]
print(f"[SERVER] Listening on {HOST}: {PORT} (Select mode enabled)")

while True:
    # select nos dice qué sockets están listos para lectura (readable)
    readable, writable, exceptional = select.select(inputs, [], [])

    for s in readable:
        if s is server:
            # Ha llegado un nuevo cliente
            connection, client_address = s.accept()
            connection.setblocking(False)
            inputs.append(connection)
            print(f"[SERVER] New connection from {client_address}")
        else:
            # Ha llegado un mensaje de un cliente ya conectado
            try:
                data = s.recv(1024)
                if data:
                    print(f"[SERVER] Received: {data}")
                    # Caso A: El cliente pide las películas
                    if data == b"GET_SCREENINGS":
                        s.sendall(screenings_response)
                        print(f"[SERVER] Sent screenings list.")
                    # Caso B: El cliente intenta comprar
                    else:
                        request_str = data.decode()
                        if request_str in screenings_data and screenings_data[request_str] > 0:
                            screenings_data[request_str] -= 1
                            result = b"SUCCESS"
                            ticket_id = generate_ticket_id()
                            print(f"[SERVER] Purchase successful! Ticket: {ticket_id.decode()}. Seats left for {request_str}: {screenings_data[request_str]}")
                        else:
                            result = b"FAIL"
                            ticket_id = b"000000"
                            print(f"[SERVER] Purchase failed for {request_str}. No seats available.")
                        # Enviamos el struct de respuesta
                        response = struct.pack('7s6s', result, ticket_id)
                        s.sendall(response)

                        # Como ya terminó la compra, desconectamos a este cliente
                        inputs.remove(s)
                        s.close()
                else:
                    # Si data está vacío, el cliente cerró la conexión
                    print(f"[SERVER] Connection closed by client.")
                    inputs.remove(s)
                    s.close()
            except ConnectionResetError:
                # Por si el cliente se desconecta abruptamente
                print(f"[SERVER] Connection reset by client.")
                inputs.remove(s)
                s.close()
