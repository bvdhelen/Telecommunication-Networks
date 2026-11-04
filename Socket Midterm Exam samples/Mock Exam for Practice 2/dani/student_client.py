# student_client_struct.py


def run_student_client(
    # Parameters
):

    print(f"Connecting to library server at <ip>:<port>...")
    print("Connected successfully!")
    print("\nAvailable actions:")
    print("  - check: Check book availability")
    print("  - borrow: Borrow a book with reservation code")
    print("  - quit: Exit\n")
    input("Enter action (check/borrow/quit): ").strip()
    print("Disconnecting from library...")
    print("Invalid action! Use 'check', 'borrow', or 'quit'")
    input("Enter book ID (8 chars): ").strip()
    input("Enter reservation code (6 chars): ").strip()
    print(f"Sent: '<message>'")
    # BONUS
    # print(f"Sent struct message (action: <action>, book_id: <book_id>)")
    print("Server closed the connection unexpectedly.")
    print(f"Response: <response_str>")
    print(f"✓ Book is available! Copies: <copies>\n")
    print("✗ Book is unavailable.\n")
    print("✓ Book borrowed successfully!\n")
    print("✗ Borrow failed! (Wrong code or no copies available)\n")
    print("Connection refused. Is the library server running?")
    print(f"An error occurred: <e>")
    print("Connection closed.")


if __name__ == "__main__":
    print("Usage: python3 student_client_struct.py <server_ip> <server_port>")
