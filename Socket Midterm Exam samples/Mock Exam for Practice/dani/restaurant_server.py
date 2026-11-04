# restaurant_server.py
import sys
import socket
import select
import json
from datetime import datetime


def load_menu_from_json(json_file):
    """Load menu from JSON file"""


def send_log_to_logger(
    # Parameters
):
    """Send order log to logger server via UDP"""
    print(f"  Logger acknowledged: <ack here>")
    print("  No ACK from logger (timeout)")
    print(f"  Error sending to logger: {e}")


def run_restaurant_server(
    # Parameters
):
    menu = {
        "PIZZ": {"name": "Margherita Pizza", "price": 1200, "stock": 10},
        "BURG": {"name": "Cheeseburger", "price": 800, "stock": 15},
        "SALA": {"name": "Caesar Salad", "price": 600, "stock": 20},
    }
    print("Restaurant Menu:")
    for item_id, info in menu.items():
        price_str = f"${info['price']/100:.2f}"
        print(f"  {item_id}: {info['name']} - {price_str}, Stock: {info['stock']}")

    print(f"\nRestaurant server listening on {ip}:{port}")
    print(f"Will log orders to {logger_ip}:{logger_port}")

    print(f"\nNew student connected from {client_addr}")
    print(f"Student <get the name of the student here> disconnected.")

    print(
        f"Student <get the name of the student here> - Action: {action}, Item: {item_id}, Qty: {quantity}"
    )

    print(f"  Response: {response}")

    print(
        f"  ORDER SUCCESS! Total: ${total_price/100:.2f}, Remaining stock: {remaining}"
    )

    print(f"  Response: {response}")

    print(f"  Unknown action: {action}")

    print(f"Invalid message from <get the name of the student here>: {e}")

    print("\nRestaurant server shutting down.")


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            "Usage: python3 restaurant_server.py <ip> <port> <menu.json> <logger_ip> <logger_port>"
        )
        sys.exit(1)
