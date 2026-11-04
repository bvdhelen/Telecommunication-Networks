# student_client.py
import sys
import socket

# --- Complete Solution: Tasks 1, 2, 3, 4 ---


def run_student_client(
    # Parameters
):
    print(f"Connecting to restaurant server at {ip}:{port}...")
    print("Connected successfully!")
    print("\nAvailable actions:")
    print("  - VIEW: View item details")
    print("  - ORDER: Place an order")
    print("  - QUIT: Exit\n")

    action = input("Enter action (VIEW/ORDER/QUIT): ").strip().upper()

    print("Disconnecting from restaurant...")

    print("Invalid action! Use VIEW, ORDER, or QUIT")

    # Get item ID
    item_id = input("Enter item ID: ").strip().upper()

    # Get quantity
    quantity = input("Enter quantity: ").strip()
    print("Quantity must be positive!")
    print("Invalid quantity!")

    print(f"Sent: {message}")

    print("Server closed the connection unexpectedly.")

    print(f"Response: {response_str}")

    print("✗ Item not found in menu.\n")
    print("✗ Error processing request.\n")
    print(f"✓ Available: {name}, Price: ${price/100:.2f}, Stock: {stock}\n")
    print(f"✗ Unexpected response format.\n")

    print(f"✓ Order placed! Total: ${total/100:.2f}\n")
    print("✗ Insufficient stock for this order.\n")
    print("✗ Item not found in menu.\n")
    print("✗ Error processing order.\n")
    print(f"✗ Unexpected response: {response_str}\n")

    print("Connection refused. Is the restaurant server running?")
    print(f"An error occurred: {e}")
    print("Connection closed.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 student_client.py <server_ip> <server_port>")
        sys.exit(1)
