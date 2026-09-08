import socket
import threading


HOST = "127.0.0.1"
PORT = 5555


class ChatClient:

    def __init__(self, username, on_message=None):
        self.username = username
        self.on_message = on_message
        self.socket = None
        self.connected = False

    def connect(self):
        try:
            self.socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            self.socket.connect(
                (HOST, PORT)
            )

            self.socket.send(
                self.username.encode("utf-8")
            )

            self.connected = True

            receiver_thread = threading.Thread(
                target=self.receive_messages,
                daemon=True
            )

            receiver_thread.start()

            return True, "Connected to server."

        except ConnectionRefusedError:
            return False, "Server is not running."

        except OSError as error:
            return False, f"Connection error: {error}"

    def send_message(self, message):

        if not self.connected:
            return False

        if not message.strip():
            return False

        try:
            self.socket.send(
                message.encode("utf-8")
            )

            return True

        except (BrokenPipeError, ConnectionResetError, OSError):
            self.connected = False
            return False

    def join_room(self, room):

        if not room.strip():
            return False

        return self.send_message(
            f"/room {room.strip()}"
        )

    def receive_messages(self):

        while self.connected:

            try:

                data = self.socket.recv(4096)

                if not data:
                    break

                message = data.decode(
                    "utf-8"
                )

                if self.on_message:
                    self.on_message(message)

            except (
                ConnectionResetError,
                BrokenPipeError,
                OSError
            ):
                break

        self.connected = False

        if self.on_message:
            self.on_message(
                "*** Disconnected from server ***"
            )

    def disconnect(self):

        self.connected = False

        if self.socket:

            try:
                self.socket.shutdown(
                    socket.SHUT_RDWR
                )
            except OSError:
                pass

            try:
                self.socket.close()
            except OSError:
                pass