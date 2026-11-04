# logger_server.py
import sys
import socket
import json
import os

# --- Complete Solution: Task 4 ---


def append_to_json_log(
    # Parameters
):
    """Append order entry to JSON log file"""
    print(f"Error writing to log file: {e}")


def run_logger_server(
    # Parameters
):
    print(f"Logger server listening on {ip}:{port}")
    print(f"Logging to file: {log_file}\n")

    print(f"Received order from {server_addr}:")
    print(f"  Time: {timestamp}")
    print(f"  Student: {student_ip}")
    print(f"  Item: {item_id}")
    print(f"  Quantity: {quantity}")
    print(f"  Total: ${total_price/100:.2f}")

    # Create log entry
    log_entry = {
        "timestamp": timestamp,
        "student_ip": student_ip,
        "item_id": item_id,
        "quantity": quantity,
        "total_price": total_price,
    }

    # Append to JSON log
    print(f"✓ Logged to {log_file}")
    print("✗ Failed to log")

    print()

    print(f"Invalid log format from {server_addr}: {e}")

    print("\nLogger server shutting down.")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 logger_server.py <listen_ip> <listen_port> <log_file>")
        sys.exit(1)
