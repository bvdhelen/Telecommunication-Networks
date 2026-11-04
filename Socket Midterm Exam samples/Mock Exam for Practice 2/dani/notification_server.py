# notification_server.py

# --- Solves Task IV (UDP notification logging) ---


def append_to_json_log(
    # Parameters
):
    """Append entry to JSON log file"""
    print(f"Error writing to log file: <e>")


def run_notification_server(
    # Parameters
):
    print(f"Notification server listening on <ip>:<port>")
    print(f"Logging to file: <log_file>\n")
    # Parse notification: "timestamp|student_ip|book_id|remaining_copies"
    print(f"Received notification from <server_addr>:")
    print(f"  Time: <timestamp>")
    print(f"  Student: <student_ip>")
    print(f"  Book: <book_id>")
    print(f"  Remaining: <remaining_copies> copies")
    # Create log entry
    log_entry = {
        "timestamp": "<timestamp>",
        "student_ip": "<student_ip>",
        "book_id": "<book_id>",
        "remaining_copies": "<remaining_copies>",
    }
    print(f"✓ Logged to <log_file>")
    print("✗ Failed to log")
    print(f"Invalid notification format from <server_addr>: <e>")
    print("\nNotification server shutting down.")


if __name__ == "__main__":
    print("Usage: python3 notification_server.py <listen_ip> <listen_port> <log_file>")
