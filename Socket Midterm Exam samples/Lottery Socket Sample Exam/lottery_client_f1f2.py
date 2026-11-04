import socket
import struct
import hashlib

HOST = '127.0.0.1'
PORT = 5000

print("--- WELCOME TO THE LOTTERY ---")
client_numbers = []
for i in range(5):
    while True:
        try:
            num = int(input(f"Enter number {i+1} (1-20): "))
            if 1 <= num <= 20:
                client_numbers.append(num)
                break
            else:
                print("Number must be between 1 and 20.")
        except ValueError:
            print("Please enter a valid integer.")

bet = int(input("Enter your bet amount: "))

# Empaquetar datos y calcular MD5
raw_data = struct.pack('!5BI', *client_numbers, bet)
md5_hash = hashlib.md5(raw_data).digest()
# Unimos el hash (16s) con los datos
packet = struct.pack('!16s', md5_hash) + raw_data

# Conectar y enviar
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print("\nSending data to server...")
client.sendall(packet)

# Recibir respuesta (25 bytes)
response = client.recv(25)
if len(response) == 25:
    received_hash, *rest = struct.unpack('!16s5BI', response)
    draw_numbers = list(rest[:5])
    winnings = rest[5]
    
    # Verificar integridad
    raw_resp = struct.pack('!5BI', *draw_numbers, winnings)
    if received_hash == hashlib.md5(raw_resp).digest():
        print("\n--- RESULTS ---")
        print(f"Drawn numbers: {draw_numbers}")
        print(f"Your numbers:  {client_numbers}")
        print(f"Your winnings: ${winnings}")
    else:
        print("Error: MD5 checksum from server is invalid.")
else:
    print("Error receiving data.")

client.close()
