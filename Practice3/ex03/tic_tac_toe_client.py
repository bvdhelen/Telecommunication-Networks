import socket
import struct

HOST, PORT = 'localhost', 10000
msg = struct.Struct("1s I I")

def send(c, t, x=0, y=0):
    c.sendall(msg.pack(t.encode(), x, y))

def recv(c):
    data = b''
    while len(data) < msg.size:
        chunk = c.recv(msg.size - len(data))
        if not chunk:
            return None
        data += chunk
    return msg.unpack(data)

def ask_move():
    while True:
        try:
            x, y = map(int, input("Introduce x y (0-2): ").split())
            return x, y
        except ValueError:
            print("Invalid format. Use: 'x y'")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))
    print("Connected to the server")

    while True:
        m = recv(client)
        if m is None:
            print("Server ends conexion")
            break
        t, x, y = m
        t = t.decode()

        if t == 'S': #START
            print("You start (X).")
            a, b = ask_move()
            send(client, 'M', a, b)

        elif t == 'W': #WAIT
            print("Waiting for the oponnent...")

        elif t == 'M': #MOVE
            print(f"The oponnent plays in ({x},{y}). Your turn.")
            a, b = ask_move()
            send(client, 'M', a, b)

        elif t == 'I': #INVALID
            print("Invalid movement, try another box.")
            a, b = ask_move()
            send(client, 'M', a, b)

        elif t == 'R': #RESULT
            if x == 1:   print("You win!")
            elif x == 0: print("You lose.")
            else:        print("Draw")
            break