import socket
import struct

HOST, PORT = 'localhost', 10000
msg = struct.Struct("1s I I")   # x, y

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

def check_winner(b):
    for i in range(3):
        if b[i][0] != ' ' and b[i][0] == b[i][1] == b[i][2]: return b[i][0]
        if b[0][i] != ' ' and b[0][i] == b[1][i] == b[2][i]: return b[0][i]
    if b[0][0] != ' ' and b[0][0] == b[1][1] == b[2][2]: return b[0][0]
    if b[0][2] != ' ' and b[0][2] == b[1][1] == b[2][0]: return b[0][2]
    if all(b[i][j] != ' ' for i in range(3) for j in range(3)): return 'D'
    return None

def print_board(b):
    for row in b:
        print(' '.join(row))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(2)
    print("Waiting for players...")

    c1, a1 = server.accept(); print("Player 1:", a1)
    c2, a2 = server.accept(); print("Player 2:", a2)

    board = [[' '] * 3 for _ in range(3)]
    players = [(c1, 'X'), (c2, 'O')]
    turn = 0

    send(c1, 'S')
    send(c2, 'W')

    while True:
        cur, sym = players[turn]
        other, _ = players[1 - turn]

        m = recv(cur)
        if m is None:
            break
        _, x, y = m

        if not (0 <= x < 3 and 0 <= y < 3) or board[x][y] != ' ':
            send(cur, 'I')
            continue

        board[x][y] = sym
        print(f"Player {sym} plays in ({x},{y})")
        print_board(board)

        w = check_winner(board)
        if w == sym:
            send(cur, 'R', 1)     # win
            send(other, 'R', 0)   # lose
            break
        elif w == 'D':
            send(cur, 'R', 2)
            send(other, 'R', 2)
            break

        send(other, 'M', x, y)
        turn = 1 - turn

    c1.close()
    c2.close()
    print("Game over :(")