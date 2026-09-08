import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database import (
    initialize_database,
    register_user,
    login_user,
    create_room,
    get_rooms,
    get_messages
)

from client import ChatClient
from chat_utils import convert_emojis, format_message


class ChatApplication:

    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Chat Application")
        self.root.geometry("900x650")
        self.root.resizable(False, False)

        initialize_database()

        self.client = None
        self.username = None
        self.current_room = "General"

        self.show_login_screen()

    # -------------------------------------------------
    # LOGIN SCREEN
    # -------------------------------------------------

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):

        self.clear_window()

        frame = ttk.Frame(
            self.root,
            padding=40
        )

        frame.pack(
            expand=True
        )

        ttk.Label(
            frame,
            text="ADVANCED CHAT APPLICATION",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        ttk.Label(
            frame,
            text="Username"
        ).pack(pady=5)

        self.username_entry = ttk.Entry(
            frame,
            width=35
        )

        self.username_entry.pack(pady=5)

        ttk.Label(
            frame,
            text="Password"
        ).pack(pady=5)

        self.password_entry = ttk.Entry(
            frame,
            width=35,
            show="*"
        )

        self.password_entry.pack(pady=5)

        ttk.Button(
            frame,
            text="LOGIN",
            command=self.login
        ).pack(pady=15)

        ttk.Button(
            frame,
            text="REGISTER",
            command=self.register
        ).pack(pady=5)

        self.login_status = ttk.Label(
            frame,
            text=""
        )

        self.login_status.pack(pady=10)

    # -------------------------------------------------
    # REGISTER
    # -------------------------------------------------

    def register(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:

            self.login_status.config(
                text="Username and password are required."
            )

            return

        if len(username) < 3:

            self.login_status.config(
                text="Username must contain at least 3 characters."
            )

            return

        if len(password) < 4:

            self.login_status.config(
                text="Password must contain at least 4 characters."
            )

            return

        success, message = register_user(
            username,
            password
        )

        self.login_status.config(
            text=message
        )

    # -------------------------------------------------
    # LOGIN
    # -------------------------------------------------

    def login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:

            self.login_status.config(
                text="Please enter username and password."
            )

            return

        if not login_user(
            username,
            password
        ):

            self.login_status.config(
                text="Invalid username or password."
            )

            return

        self.username = username

        self.connect_to_server()

    # -------------------------------------------------
    # CONNECT TO SERVER
    # -------------------------------------------------

    def connect_to_server(self):

        self.client = ChatClient(
            self.username,
            self.receive_message
        )

        success, message = self.client.connect()

        if not success:

            messagebox.showerror(
                "Connection Error",
                message
            )

            return

        self.show_chat_screen()

    # -------------------------------------------------
    # CHAT SCREEN
    # -------------------------------------------------

    def show_chat_screen(self):

        self.clear_window()

        # MAIN FRAME

        main_frame = ttk.Frame(
            self.root,
            padding=10
        )

        main_frame.pack(
            fill="both",
            expand=True
        )

        # HEADER

        header = ttk.Frame(
            main_frame
        )

        header.pack(
            fill="x",
            pady=(0, 10)
        )

        ttk.Label(
            header,
            text=f"Welcome, {self.username}",
            font=("Arial", 15, "bold")
        ).pack(
            side="left"
        )

        ttk.Button(
            header,
            text="Logout",
            command=self.logout
        ).pack(
            side="right"
        )

        # CONTENT

        content = ttk.Frame(
            main_frame
        )

        content.pack(
            fill="both",
            expand=True
        )

        # ROOM PANEL

        room_frame = ttk.LabelFrame(
            content,
            text="Chat Rooms",
            padding=10
        )

        room_frame.pack(
            side="left",
            fill="y",
            padx=(0, 10)
        )

        self.room_listbox = tk.Listbox(
            room_frame,
            width=20,
            height=25
        )

        self.room_listbox.pack(
            pady=5
        )

        self.room_listbox.bind(
            "<<ListboxSelect>>",
            self.room_selected
        )

        ttk.Button(
            room_frame,
            text="Refresh Rooms",
            command=self.load_rooms
        ).pack(
            pady=5
        )

        ttk.Button(
            room_frame,
            text="Create Room",
            command=self.create_new_room
        ).pack(
            pady=5
        )

        # CHAT PANEL

        chat_frame = ttk.Frame(
            content
        )

        chat_frame.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.room_label = ttk.Label(
            chat_frame,
            text="Room: General",
            font=("Arial", 14, "bold")
        )

        self.room_label.pack(
            pady=5
        )

        self.chat_display = tk.Text(
            chat_frame,
            height=24,
            width=65,
            state="disabled",
            wrap="word"
        )

        self.chat_display.pack(
            fill="both",
            expand=True
        )

        # MESSAGE AREA

        message_frame = ttk.Frame(
            chat_frame
        )

        message_frame.pack(
            fill="x",
            pady=10
        )

        self.message_entry = ttk.Entry(
            message_frame
        )

        self.message_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )

        self.message_entry.bind(
            "<Return>",
            lambda event: self.send_message()
        )

        ttk.Button(
            message_frame,
            text="Send",
            command=self.send_message
        ).pack(
            side="right"
        )

        ttk.Label(
            chat_frame,
            text="Emoji shortcuts: :smile: :heart: :laugh: :thumbsup: :fire:"
        ).pack(
            pady=2
        )

        # STATUS

        self.status_label = ttk.Label(
            main_frame,
            text="Connected"
        )

        self.status_label.pack(
            pady=5
        )

        self.load_rooms()
        self.load_message_history("General")

    # -------------------------------------------------
    # LOAD ROOMS
    # -------------------------------------------------

    def load_rooms(self):

        rooms = get_rooms()

        self.room_listbox.delete(
            0,
            tk.END
        )

        for room in rooms:

            self.room_listbox.insert(
                tk.END,
                room
            )

    # -------------------------------------------------
    # CREATE ROOM
    # -------------------------------------------------

    def create_new_room(self):

        dialog = tk.Toplevel(
            self.root
        )

        dialog.title(
            "Create Room"
        )

        dialog.geometry(
            "300x150"
        )

        ttk.Label(
            dialog,
            text="Room name:"
        ).pack(
            pady=10
        )

        room_entry = ttk.Entry(
            dialog,
            width=30
        )

        room_entry.pack()

        def save_room():

            room_name = room_entry.get().strip()

            success, message = create_room(
                room_name
            )

            if success:

                dialog.destroy()

                self.load_rooms()

            else:

                messagebox.showerror(
                    "Room Error",
                    message
                )

        ttk.Button(
            dialog,
            text="Create",
            command=save_room
        ).pack(
            pady=10
        )

    # -------------------------------------------------
    # SELECT ROOM
    # -------------------------------------------------

    def room_selected(self, event):

        selection = self.room_listbox.curselection()

        if not selection:
            return

        room = self.room_listbox.get(
            selection[0]
        )

        self.current_room = room

        self.room_label.config(
            text=f"Room: {room}"
        )

        if self.client:
            self.client.join_room(room)

        self.load_message_history(room)

    # -------------------------------------------------
    # LOAD MESSAGE HISTORY
    # -------------------------------------------------

    def load_message_history(self, room):

        messages = get_messages(
            room
        )

        self.chat_display.config(
            state="normal"
        )

        self.chat_display.delete(
            "1.0",
            tk.END
        )

        for username, message, timestamp in messages:

            message = convert_emojis(
                message
            )

            formatted = format_message(
                username,
                message,
                timestamp
            )

            self.chat_display.insert(
                tk.END,
                formatted + "\n"
            )

        self.chat_display.config(
            state="disabled"
        )

        self.chat_display.see(
            tk.END
        )

    # -------------------------------------------------
    # SEND MESSAGE
    # -------------------------------------------------

    def send_message(self):

        message = self.message_entry.get().strip()

        if not message:
            return

        if not self.client or not self.client.connected:

            messagebox.showerror(
                "Connection Error",
                "You are not connected to the server."
            )

            return

        self.client.send_message(
            message
        )

        self.message_entry.delete(
            0,
            tk.END
        )

    # -------------------------------------------------
    # RECEIVE MESSAGE
    # -------------------------------------------------

    def receive_message(self, message):

        self.root.after(
            0,
            lambda: self.process_received_message(
                message
            )
        )

    def process_received_message(self, message):

        # Server notification
        if message.startswith("***"):

            self.display_message(
                message
            )

            return

        parts = message.split(
            "|",
            2
        )

        if len(parts) != 3:
            return

        username, room, text = parts

        if room != self.current_room:
            return

        text = convert_emojis(
            text
        )

        timestamp = datetime.now().strftime(
            "%H:%M"
        )

        formatted = format_message(
            username,
            text,
            timestamp
        )

        self.display_message(
            formatted
        )

        # Notification
        if username != self.username:

            self.root.bell()

            self.status_label.config(
                text=f"New message from {username}"
            )

    # -------------------------------------------------
    # DISPLAY MESSAGE
    # -------------------------------------------------

    def display_message(self, message):

        self.chat_display.config(
            state="normal"
        )

        self.chat_display.insert(
            tk.END,
            message + "\n"
        )

        self.chat_display.config(
            state="disabled"
        )

        self.chat_display.see(
            tk.END
        )

    # -------------------------------------------------
    # LOGOUT
    # -------------------------------------------------

    def logout(self):

        if self.client:

            self.client.disconnect()

        self.client = None
        self.username = None

        self.show_login_screen()


def start_application():

    root = tk.Tk()

    ChatApplication(
        root
    )

    root.mainloop()


if __name__ == "__main__":
    start_application()