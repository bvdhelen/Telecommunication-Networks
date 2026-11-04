# logger_server.py
import sys
import socket
import json
import os

# --- Complete Solution: Task 4 ---


def append_to_json_log(log_file, entry):
    """Append order entry to JSON log file"""
    try:
        # Read existing data
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                data = json.load(f)
        else:
            data = []

        # Append new entry
        data.append(entry)

        # Write back
        with open(log_file, "w") as f:
            json.dump(data, f, indent=2)

        return True
    except Exception as e:
        print(f"Error writing to log file: {e}")
        return False


def run_logger_server(ip, port, log_file):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((ip, port))
        print(f"Logger server listening on {ip}:{port}")
        print(f"Logging to file: {log_file}\n")

        try:
            while True:
                data, server_addr = sock.recvfrom(1024)

                # Parse log message: "timestamp|student_ip|item_id|quantity|total_price"
                try:
                    parts = data.decode().split("|")
                    timestamp = parts[0]
                    student_ip = parts[1]
                    item_id = parts[2]
                    quantity = int(parts[3])
                    total_price = int(parts[4])

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
                    if append_to_json_log(log_file, log_entry):
                        print(f"✓ Logged to {log_file}")
                        sock.sendto(b"ACK", server_addr)
                    else:
                        print("✗ Failed to log")
                        sock.sendto(b"ERROR", server_addr)

                    print()

                except (ValueError, IndexError) as e:
                    print(f"Invalid log format from {server_addr}: {e}")

        except KeyboardInterrupt:
            print("\nLogger server shutting down.")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 logger_server.py <listen_ip> <listen_port> <log_file>")
        sys.exit(1)

    listen_ip = sys.argv[1]
    listen_port = int(sys.argv[2])
    log_file = sys.argv[3]

    run_logger_server(listen_ip, listen_port, log_file)
