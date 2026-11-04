#Elena Sol Díaz Contreras
#Assignment3 - Question, Answer

import socket
import struct
import time
import random
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: py client.py <server_address> <server_port>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    # Create TCP socket and connect
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
    except ConnectionRefusedError:
        print("Could not connect to the server. Make sure it is running.")
        sys.exit(1)
    print("Connected to the server. Starting search...")

    # Limits for binary search (1 to 100)
    low = 1
    high = 100

    try:
        while low <= high:
            # Wait between 1 and 5 seconds before every new guess
            time.sleep(random.uniform(1.0, 5.0))

            # If limits meet, we found the exact number
            if low == high:
                guess = low
                op = b'=' # Operator for equal
            else:
                guess = (low + high) // 2
                # Ask if the secret number is greater than our guess
                op = b'>'

            # Pack and send the message
            msg = struct.pack('ci', op, guess)
            client_socket.sendall(msg)

            # Print to console what we are asking
            print(f"Sending: {op.decode()} {guess}")

            # Receive response
            data = client_socket.recv(1024)
            if not data:
                break

            resp_op, _ = struct.unpack('ci', data)
            resp_char = resp_op.decode()

            print(f"Server response: {resp_char}")

            # Evaluate the response
            if resp_char == 'Y':
                print("I won!")
                break
            elif resp_char == 'K':
                print("I guessed wrong using '='. I lost.")
                break
            elif resp_char == 'V':
                print("Game over (another client won).")
                break
            elif resp_char == 'I': # Yes, the secret number is greater
                low = guess + 1
            elif resp_char == 'N': # No, the secret number is NOT greater (smaller or equal)
                high = guess

    except KeyboardInterrupt:
        # Catch Ctrl+C gracefully
        print("\nCtrl+C pressed. Disconnecting from the server...")

    # Terminate connection
    finally:
        # This block always runs: whether we break the loop, finish normally, or press Ctrl+C
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()

# Submission:
    # Send it to the TMS in .zip file which should contain a client.py and a server.py only!
