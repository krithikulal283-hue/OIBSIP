import socket
import threading

from database import (
    initialize_database,
    save_message
)


HOST = "127.0.0.1"
PORT = 5555

clients = {}
clients_lock = threading.Lock()


def broadcast(message, exclude_client=None):
    """Send a message to all connected clients."""

    with clients_lock:

        disconnected_clients = []

        for client_socket in clients:

            if client_socket == exclude_client:
                continue

            try:
                client_socket.send(
                    message.encode("utf-8")
                )

            except (ConnectionResetError, BrokenPipeError, OSError):
                disconnected_clients.append(client_socket)

        for client_socket in disconnected_clients:

            clients.pop(
                client_socket,
                None
            )


def handle_client(client_socket, address):
    """Handle communication with one connected client."""

    username = None
    room = "General"

    try:

        # Receive username
        username = client_socket.recv(1024).decode(
            "utf-8"
        ).strip()

        if not username:
            return

        with clients_lock:
            clients[client_socket] = username

        join_message = (
            f"*** {username} joined the chat ***"
        )

        print(join_message)

        broadcast(
            join_message,
            exclude_client=client_socket
        )

        while True:

            data = client_socket.recv(4096)

            if not data:
                break

            message = data.decode(
                "utf-8"
            ).strip()

            if not message:
                continue

            # Room command
            if message.startswith("/room "):

                new_room = message[6:].strip()

                if new_room:
                    room = new_room

                    response = (
                        f"*** You joined room: {room} ***"
                    )

                    client_socket.send(
                        response.encode("utf-8")
                    )

                continue

            # Regular message
            formatted_message = (
                f"{username}|{room}|{message}"
            )

            print(
                f"[{room}] {username}: {message}"
            )

            # Save message
            save_message(
                username,
                room,
                message
            )

            broadcast(
                formatted_message,
                exclude_client=client_socket
            )

            # Send the message back to sender
            try:

                client_socket.send(
                    formatted_message.encode("utf-8")
                )

            except OSError:
                break

    except (ConnectionResetError, BrokenPipeError, OSError):
        pass

    finally:

        with clients_lock:
            clients.pop(
                client_socket,
                None
            )

        try:
            client_socket.close()
        except OSError:
            pass

        if username:

            leave_message = (
                f"*** {username} left the chat ***"
            )

            print(leave_message)

            broadcast(
                leave_message
            )


def start_server():

    initialize_database()

    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server_socket.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server_socket.bind(
        (HOST, PORT)
    )

    server_socket.listen(10)

    print("=" * 50)
    print("       ADVANCED CHAT SERVER")
    print("=" * 50)
    print(
        f"Server running on {HOST}:{PORT}"
    )
    print("Waiting for clients...")
    print("Press CTRL+C to stop the server.")
    print("=" * 50)

    try:

        while True:

            client_socket, address = (
                server_socket.accept()
            )

            print(
                f"New connection from {address}"
            )

            client_thread = threading.Thread(
                target=handle_client,
                args=(
                    client_socket,
                    address
                ),
                daemon=True
            )

            client_thread.start()

    except KeyboardInterrupt:

        print("\nServer shutting down...")

    finally:

        with clients_lock:

            for client_socket in clients:

                try:
                    client_socket.close()
                except OSError:
                    pass

            clients.clear()

        server_socket.close()


if __name__ == "__main__":
    start_server()