import socket
import struct

HOST = '127.0.0.1'
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# 1. Enviar GET_SCREENINGS
print("Sending: GET_SCREENINGS")
client.sendall(b"GET_SCREENINGS")

# 2. Recibir y mostrar screenings
data = client.recv(1024).decode()
print("Received screenings:")
for screening in data.split('|'):
    title, hall, time = screening.split(';')
    print(f"\t{title}, {hall}, {time}")

# 3. Enviar petición (Hardcodeada para el ejemplo)
request = "Dune;17:30"
print(f"Buying ticket: Dune 17:30")
client.sendall(request.encode())

# 4. Recibir respuesta en struct
response = client.recv(1024)
result, ticket_id = struct.unpack('7s6s', response)

# Limpiamos los bytes nulos que pueda tener el string de 7s
result_str = result.decode().strip('\x00') 
ticket_str = ticket_id.decode().strip('\x00')

if result_str == "SUCCESS":
    print(f"Purchase successful, ticket ID: {ticket_str}")
else:
    print("Purchase failed.")

client.close()
