# restaurant_server.py
import sys
import socket
import select
import json
from datetime import datetime

# --- Complete Solution: Tasks 1, 2, 3, 4 ---


def load_menu_from_json(json_file):
    """Load menu from JSON file"""
    try:
        with open(json_file, "r") as f:
            menu_list = json.load(f)

        menu = {}
        for item in menu_list:
            item_id = item["item_id"]
            menu[item_id] = {
                "name": item["name"],
                "price": item["price"],
                "stock": item["stock"],
            }
        return menu
    except FileNotFoundError:
        print(f"Error: Menu file '{json_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{json_file}'.")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: Missing field in menu: {e}")
        sys.exit(1)


def send_log_to_logger(
    udp_sock, logger_addr, student_ip, item_id, quantity, total_price
):
    """Send order log to logger server via UDP"""
    try:
        timestamp = datetime.now().isoformat()
        message = f"{timestamp}|{student_ip}|{item_id}|{quantity}|{total_price}"
        udp_sock.sendto(message.encode(), logger_addr)

        # Wait for ACK
        udp_sock.settimeout(1.0)
        try:
            ack, _ = udp_sock.recvfrom(1024)
            print(f"  Logger acknowledged: {ack.decode()}")
        except socket.timeout:
            print("  No ACK from logger (timeout)")
    except Exception as e:
        print(f"  Error sending to logger: {e}")


def run_restaurant_server(ip, port, json_file, logger_ip, logger_port):
    # Load menu from JSON
    menu = load_menu_from_json(json_file)

    print("Restaurant Menu:")
    for item_id, info in menu.items():
        price_str = f"${info['price']/100:.2f}"
        print(f"  {item_id}: {info['name']} - {price_str}, Stock: {info['stock']}")

    # TCP server socket
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((ip, port))
    server_sock.listen(5)

    # UDP socket for logger
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    logger_address = (logger_ip, logger_port)

    inputs = [server_sock]

    print(f"\nRestaurant server listening on {ip}:{port}")
    print(f"Will log orders to {logger_ip}:{logger_port}")

    try:
        while True:
            readables, _, _ = select.select(inputs, [], [])

            for s in readables:
                if s is server_sock:
                    connection, client_addr = s.accept()
                    print(f"\nNew student connected from {client_addr}")
                    inputs.append(connection)
                else:
                    data = s.recv(1024)
                    if not data:
                        print(f"Student {s.getpeername()} disconnected.")
                        inputs.remove(s)
                        s.close()
                    else:
                        try:
                            # Parse message: "action|item_id|quantity"
                            message = data.decode().strip()
                            parts = message.split("|")

                            if len(parts) != 3:
                                s.sendall(b"ERROR")
                                continue

                            action = parts[0]
                            item_id = parts[1]
                            quantity = int(parts[2])

                            print(
                                f"Student {s.getpeername()} - Action: {action}, Item: {item_id}, Qty: {quantity}"
                            )

                            if action == "VIEW":
                                if item_id in menu:
                                    info = menu[item_id]
                                    response = f"{info['name']}:{info['price']}:{info['stock']}"
                                else:
                                    response = "NOT_FOUND"
                                s.sendall(response.encode())
                                print(f"  Response: {response}")

                            elif action == "ORDER":
                                if item_id not in menu:
                                    response = "NOT_FOUND"
                                elif menu[item_id]["stock"] < quantity:
                                    response = "NO_STOCK"
                                elif quantity <= 0:
                                    response = "ERROR"
                                else:
                                    # Process order
                                    menu[item_id]["stock"] -= quantity
                                    total_price = menu[item_id]["price"] * quantity
                                    response = f"SUCCESS:{total_price}"

                                    student_ip = s.getpeername()[0]
                                    remaining = menu[item_id]["stock"]

                                    print(
                                        f"  ORDER SUCCESS! Total: ${total_price/100:.2f}, Remaining stock: {remaining}"
                                    )

                                    # Send to logger
                                    send_log_to_logger(
                                        udp_sock,
                                        logger_address,
                                        student_ip,
                                        item_id,
                                        quantity,
                                        total_price,
                                    )

                                s.sendall(response.encode())
                                print(f"  Response: {response}")

                            else:
                                s.sendall(b"ERROR")
                                print(f"  Unknown action: {action}")

                        except (ValueError, IndexError) as e:
                            print(f"Invalid message from {s.getpeername()}: {e}")
                            s.sendall(b"ERROR")

    except KeyboardInterrupt:
        print("\nRestaurant server shutting down.")
    finally:
        for s in inputs:
            s.close()
        udp_sock.close()


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            "Usage: python3 restaurant_server.py <ip> <port> <menu.json> <logger_ip> <logger_port>"
        )
        sys.exit(1)

    listen_ip = sys.argv[1]
    listen_port = int(sys.argv[2])
    menu_json = sys.argv[3]
    logger_ip = sys.argv[4]
    logger_port = int(sys.argv[5])

    run_restaurant_server(listen_ip, listen_port, menu_json, logger_ip, logger_port)
