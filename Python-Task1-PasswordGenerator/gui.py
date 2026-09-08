import tkinter as tk
from tkinter import ttk, messagebox

from password_generator import (
    generate_password,
    calculate_strength
)

from history import PasswordHistory


class PasswordGeneratorGUI:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Advanced Random Password Generator"
        )

        self.root.geometry(
            "800x650"
        )

        self.root.resizable(
            False,
            False
        )

        self.history = PasswordHistory()

        self.create_widgets()

    def create_widgets(self):

        # TITLE
        title = tk.Label(
            self.root,
            text="ADVANCED PASSWORD GENERATOR",
            font=("Arial", 22, "bold")
        )

        title.pack(pady=20)

        # SETTINGS FRAME
        settings_frame = ttk.LabelFrame(
            self.root,
            text="Password Settings",
            padding=20
        )

        settings_frame.pack(
            padx=30,
            fill="x"
        )

        # LENGTH
        ttk.Label(
            settings_frame,
            text="Password Length:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=10,
            pady=10
        )

        self.length_entry = ttk.Entry(
            settings_frame,
            width=25
        )

        self.length_entry.insert(
            0,
            "12"
        )

        self.length_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        # CHECKBOXES

        self.uppercase_var = tk.BooleanVar(
            value=True
        )

        self.lowercase_var = tk.BooleanVar(
            value=True
        )

        self.number_var = tk.BooleanVar(
            value=True
        )

        self.special_var = tk.BooleanVar(
            value=True
        )

        ttk.Checkbutton(
            settings_frame,
            text="Uppercase (A-Z)",
            variable=self.uppercase_var
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        ttk.Checkbutton(
            settings_frame,
            text="Lowercase (a-z)",
            variable=self.lowercase_var
        ).grid(
            row=1,
            column=1,
            padx=10,
            pady=5,
            sticky="w"
        )

        ttk.Checkbutton(
            settings_frame,
            text="Numbers (0-9)",
            variable=self.number_var
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        ttk.Checkbutton(
            settings_frame,
            text="Special Characters",
            variable=self.special_var
        ).grid(
            row=2,
            column=1,
            padx=10,
            pady=5,
            sticky="w"
        )

        # GENERATE BUTTON

        ttk.Button(
            settings_frame,
            text="GENERATE PASSWORD",
            command=self.generate
        ).grid(
            row=3,
            column=0,
            columnspan=2,
            pady=15
        )

        # RESULT FRAME

        result_frame = ttk.LabelFrame(
            self.root,
            text="Generated Password",
            padding=20
        )

        result_frame.pack(
            padx=30,
            pady=15,
            fill="x"
        )

        self.password_entry = ttk.Entry(
            result_frame,
            width=55,
            font=("Arial", 13)
        )

        self.password_entry.pack(
            pady=10
        )

        # COPY BUTTON

        ttk.Button(
            result_frame,
            text="COPY PASSWORD",
            command=self.copy_password
        ).pack(
            pady=5
        )

        # STRENGTH

        self.strength_label = ttk.Label(
            result_frame,
            text="Strength: --",
            font=("Arial", 13, "bold")
        )

        self.strength_label.pack(
            pady=10
        )

        # HISTORY FRAME

        history_frame = ttk.LabelFrame(
            self.root,
            text="Session History",
            padding=10
        )

        history_frame.pack(
            padx=30,
            pady=5,
            fill="both",
            expand=True
        )

        columns = (
            "Password",
            "Strength",
            "Date & Time"
        )

        self.history_tree = ttk.Treeview(
            history_frame,
            columns=columns,
            show="headings",
            height=6
        )

        for column in columns:

            self.history_tree.heading(
                column,
                text=column
            )

            self.history_tree.column(
                column,
                width=220,
                anchor="center"
            )

        self.history_tree.pack(
            fill="both",
            expand=True
        )

        ttk.Button(
            history_frame,
            text="CLEAR HISTORY",
            command=self.clear_history
        ).pack(
            pady=8
        )

    # GENERATE PASSWORD

    def generate(self):

        try:

            length = int(
                self.length_entry.get()
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Length",
                "Password length must be a number."
            )

            return

        try:

            password = generate_password(
                length,
                self.uppercase_var.get(),
                self.lowercase_var.get(),
                self.number_var.get(),
                self.special_var.get()
            )

            strength = calculate_strength(
                password
            )

            self.password_entry.delete(
                0,
                tk.END
            )

            self.password_entry.insert(
                0,
                password
            )

            self.strength_label.config(
                text=f"Strength: {strength}"
            )

            self.history.add_password(
                password,
                strength
            )

            self.update_history()

        except ValueError as error:

            messagebox.showerror(
                "Invalid Settings",
                str(error)
            )

    # COPY PASSWORD

    def copy_password(self):

        password = self.password_entry.get()

        if not password:

            messagebox.showwarning(
                "No Password",
                "Please generate a password first."
            )

            return

        self.root.clipboard_clear()

        self.root.clipboard_append(
            password
        )

        self.root.update()

        messagebox.showinfo(
            "Copied",
            "Password copied to clipboard."
        )

    # UPDATE HISTORY

    def update_history(self):

        for item in self.history_tree.get_children():

            self.history_tree.delete(item)

        for record in self.history.get_history():

            self.history_tree.insert(
                "",
                "end",
                values=(
                    record["password"],
                    record["strength"],
                    record["date_time"]
                )
            )

    # CLEAR HISTORY

    def clear_history(self):

        self.history.clear_history()

        self.update_history()