# student_client.py
import sys
import socket

# --- Complete Solution: Tasks 1, 2, 3, 4 ---


def run_student_client(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            print(f"Connecting to restaurant server at {ip}:{port}...")
            sock.connect((ip, port))
            print("Connected successfully!")
            print("\nAvailable actions:")
            print("  - VIEW: View item details")
            print("  - ORDER: Place an order")
            print("  - QUIT: Exit\n")

            while True:
                # Get action
                action = input("Enter action (VIEW/ORDER/QUIT): ").strip().upper()

                if action == "QUIT":
                    print("Disconnecting from restaurant...")
                    break

                if action not in ["VIEW", "ORDER"]:
                    print("Invalid action! Use VIEW, ORDER, or QUIT")
                    continue

                # Get item ID
                item_id = input("Enter item ID: ").strip().upper()

                # Get quantity
                if action == "VIEW":
                    quantity = "0"
                else:
                    quantity = input("Enter quantity: ").strip()
                    try:
                        qty_int = int(quantity)
                        if qty_int <= 0:
                            print("Quantity must be positive!")
                            continue
                    except ValueError:
                        print("Invalid quantity!")
                        continue

                # Send message: "action|item_id|quantity"
                message = f"{action}|{item_id}|{quantity}"
                sock.sendall(message.encode())
                print(f"Sent: {message}")

                # Receive response
                response = sock.recv(1024)
                if not response:
                    print("Server closed the connection unexpectedly.")
                    break

                response_str = response.decode()
                print(f"Response: {response_str}")

                # Parse and display
                if action == "VIEW":
                    if response_str == "NOT_FOUND":
                        print("✗ Item not found in menu.\n")
                    elif response_str == "ERROR":
                        print("✗ Error processing request.\n")
                    else:
                        parts = response_str.split(":")
                        if len(parts) == 3:
                            name = parts[0]
                            price = int(parts[1])
                            stock = int(parts[2])
                            print(
                                f"✓ Available: {name}, Price: ${price/100:.2f}, Stock: {stock}\n"
                            )
                        else:
                            print(f"✗ Unexpected response format.\n")

                elif action == "ORDER":
                    if response_str.startswith("SUCCESS:"):
                        total = int(response_str.split(":")[1])
                        print(f"✓ Order placed! Total: ${total/100:.2f}\n")
                    elif response_str == "NO_STOCK":
                        print("✗ Insufficient stock for this order.\n")
                    elif response_str == "NOT_FOUND":
                        print("✗ Item not found in menu.\n")
                    elif response_str == "ERROR":
                        print("✗ Error processing order.\n")
                    else:
                        print(f"✗ Unexpected response: {response_str}\n")

        except ConnectionRefusedError:
            print("Connection refused. Is the restaurant server running?")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print("Connection closed.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 student_client.py <server_ip> <server_port>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    run_student_client(server_ip, server_port)
