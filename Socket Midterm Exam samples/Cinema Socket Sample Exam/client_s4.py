import socket
import struct

HOST = '127.0.0.1'
PORT = 12346 # OJO! Nos conectamos al Proxy, no al servidor real

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# 1. Pedir screenings
print("Sending: GET_SCREENINGS")
client.sendall(b"GET_SCREENINGS")

# 2. Recibir y mostrar screenings
data = client.recv(1024).decode()
print("Received screenings:")
for screening in data.split('|'):
    title, hall, time = screening.split(';')
    print(f"\t{title}, {hall}, {time}")

# 3. Pedir al usuario qué quiere comprar
print("\nFormat example: Dune;17:30")
request = input("Enter movie title and time to buy: ")
print(f"Buying ticket: {request}")
client.sendall(request.encode())

# 4. Recibir respuesta en struct
response = client.recv(1024)
result, ticket_id = struct.unpack('7s6s', response)

# Limpiamos los bytes nulos (\x00) que se usan para rellenar el struct
result_str = result.decode().strip('\x00') 
ticket_str = ticket_id.decode().strip('\x00')

if result_str == "SUCCESS":
    print(f"Purchase successful, ticket ID: {ticket_str}")
else:
    print(f"Purchase failed. (Result: {result_str}, ID: {ticket_str})")

client.close()
