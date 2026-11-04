import socket
import struct
import hashlib

# --- OJO: Ahora apuntamos al Proxy en el puerto 6000 ---
PROXY_HOST = '127.0.0.1'
PROXY_PORT = 6000

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
packet = struct.pack('!16s', md5_hash) + raw_data

# --- CREAMOS SOCKET UDP ---
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("\nSending data to History Proxy (UDP)...")
# Enviamos con sendto en lugar de sendall
client.sendto(packet, (PROXY_HOST, PROXY_PORT))

# Recibimos la respuesta con recvfrom
response, _ = client.recvfrom(1024)
if len(response) == 25:
    received_hash, *rest = struct.unpack('!16s5BI', response)
    draw_numbers = list(rest[:5])
    winnings = rest[5]
    
    # Verificamos integridad
    raw_resp = struct.pack('!5BI', *draw_numbers, winnings)
    if received_hash == hashlib.md5(raw_resp).digest():
        print("\n--- RESULTS ---")
        print(f"Drawn numbers: {draw_numbers}")
        print(f"Your numbers:  {client_numbers}")
        print(f"Your winnings: ${winnings}")
        
        hits = sum(1 for n in client_numbers if n in draw_numbers)
        print(f"You got {hits} hit(s)!")
    else:
        print("Error: MD5 checksum from server is invalid.")
else:
    print("Error receiving data.")

client.close()
