# library_server_task1.py


def generate_reservation_code(
    # Parameters
):
    """Generate 6 random alphanumeric characters"""


# Task IIb
# def generate_books(
#     # Parameters
# ):
#     """Generate random book inventory"""
#     titles = [
#         "Algorithms",
#         "Databases",
#         "Operating Systems",
#         "Computer Networks",
#         "Software Engineering",
#     ]

# BONUS
# def load_books_from_json(
#    # Parameters
# ):
#     """Load book inventory from JSON file and add reservation codes"""

# Task IV
# def send_notification(
#     # Parameters
# ):
#     """Send borrowing notification to the Notification System"""
#     print(f"Notification acknowledged: <ack>")
#     print("No ACK from notification system")
#     print(f"Error sending notification: <e>")


def run_library_server(
    # Parameters
):
    # Hardcoded books for Task I
    books = {
        "BOOK0001": {
            "title": "Network Programming",
            "copies": 3,
            "reservation_code": "<reservation_code>",
        },
        "BOOK0002": {
            "title": "Data Structures",
            "copies": 5,
            "reservation_code": "<reservation_code>",
        },
        "BOOK0003": {
            "title": "Algorithms",
            "copies": 2,
            "reservation_code": "<reservation_code>",
        },
    }

    print("Library inventory:")
    print(f"  <book_id>: <'title'> - <'copies'> copies (code: <'reservation_code'>)")
    print(f"\nLibrary server listening on <ip>:<port>")
    # Task 4
    # print(f"Will send notifications to <notification_ip>:<notification_port>")
    print(f"\nNew student connected from <client_addr>")
    print(f"Student <peername> disconnected.")
    print(f"Student <peername> - Action: <action>, Book: <book_id>")
    response = f"available:<books>"
    response = "unavailable"
    print(f"  Response: <response>")
    response = "failed"
    response = "success"
    print(f"  SUCCESS! Book borrowed. Remaining copies: <remaining>")
    print(f"  Response: <response>")
    print(f"Invalid message format from <peername>: <e>")
    print("\nLibrary server shutting down.")


if __name__ == "__main__":
    print(
        "Usage: python3 library_server_random.py <listen_ip> <listen_port> <num_books> <notification_ip> <notification_port>"
    )
