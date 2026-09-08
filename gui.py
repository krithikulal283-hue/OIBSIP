import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt

from bmi_calculator import (
    calculate_bmi,
    get_bmi_category,
    validate_input
)

from database import (
    save_record,
    get_users,
    get_user_records
)


class BMICalculatorGUI:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Advanced BMI Calculator"
        )

        self.root.geometry(
            "900x700"
        )

        self.root.resizable(
            False,
            False
        )

        self.create_styles()
        self.create_widgets()
        self.refresh_users()

    # ---------------- STYLES ----------------

    def create_styles(self):

        style = ttk.Style()

        style.configure(
            "Title.TLabel",
            font=("Arial", 24, "bold")
        )

        style.configure(
            "Heading.TLabel",
            font=("Arial", 13, "bold")
        )

        style.configure(
            "TButton",
            font=("Arial", 11, "bold"),
            padding=8
        )

    # ---------------- WIDGETS ----------------

    def create_widgets(self):

        title = ttk.Label(
            self.root,
            text="ADVANCED BMI CALCULATOR",
            style="Title.TLabel"
        )

        title.pack(pady=20)

        # INPUT FRAME

        input_frame = ttk.LabelFrame(
            self.root,
            text="Personal Details",
            padding=20
        )

        input_frame.pack(
            padx=30,
            fill="x"
        )

        ttk.Label(
            input_frame,
            text="User Name:"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.name_entry = ttk.Entry(
            input_frame,
            width=35
        )

        self.name_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        ttk.Label(
            input_frame,
            text="Weight (kg):"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.weight_entry = ttk.Entry(
            input_frame,
            width=35
        )

        self.weight_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=10
        )

        ttk.Label(
            input_frame,
            text="Height (cm):"
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.height_entry = ttk.Entry(
            input_frame,
            width=35
        )

        self.height_entry.grid(
            row=2,
            column=1,
            padx=10,
            pady=10
        )

        ttk.Button(
            input_frame,
            text="CALCULATE BMI",
            command=self.calculate_bmi
        ).grid(
            row=3,
            column=0,
            columnspan=2,
            pady=15
        )

        # RESULT FRAME

        result_frame = ttk.LabelFrame(
            self.root,
            text="BMI Result",
            padding=15
        )

        result_frame.pack(
            padx=30,
            pady=15,
            fill="x"
        )

        self.bmi_label = ttk.Label(
            result_frame,
            text="BMI: --",
            font=("Arial", 18, "bold")
        )

        self.bmi_label.pack(
            pady=5
        )

        self.category_label = ttk.Label(
            result_frame,
            text="Category: --",
            font=("Arial", 16, "bold")
        )

        self.category_label.pack(
            pady=5
        )

        # HISTORY FRAME

        history_frame = ttk.LabelFrame(
            self.root,
            text="BMI History",
            padding=10
        )

        history_frame.pack(
            padx=30,
            pady=5,
            fill="both",
            expand=True
        )

        controls = ttk.Frame(
            history_frame
        )

        controls.pack(
            fill="x",
            pady=5
        )

        ttk.Label(
            controls,
            text="Select User:"
        ).pack(
            side="left",
            padx=5
        )

        self.user_combo = ttk.Combobox(
            controls,
            width=25,
            state="readonly"
        )

        self.user_combo.pack(
            side="left",
            padx=5
        )

        ttk.Button(
            controls,
            text="View History",
            command=self.view_history
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            controls,
            text="View BMI Trend",
            command=self.show_trend
        ).pack(
            side="left",
            padx=5
        )

        # TABLE

        table_frame = ttk.Frame(
            history_frame
        )

        table_frame.pack(
            fill="both",
            expand=True
        )

        columns = (
            "Date",
            "Weight",
            "Height",
            "BMI",
            "Category"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:

            self.tree.heading(
                column,
                text=column
            )

            self.tree.column(
                column,
                width=150,
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

    # ---------------- CALCULATE ----------------

    def calculate_bmi(self):

        name = self.name_entry.get()
        weight = self.weight_entry.get()
        height = self.height_entry.get()

        valid, message = validate_input(
            name,
            weight,
            height
        )

        if not valid:

            messagebox.showerror(
                "Invalid Input",
                message
            )

            return

        weight = float(weight)
        height = float(height)

        bmi = calculate_bmi(
            weight,
            height
        )

        category = get_bmi_category(
            bmi
        )

        self.bmi_label.config(
            text=f"BMI: {bmi:.2f}"
        )

        self.category_label.config(
            text=f"Category: {category}"
        )

        self.set_category_colour(
            category
        )

        date_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        try:

            save_record(
                name.strip(),
                weight,
                height,
                bmi,
                category,
                date_time
            )

            self.refresh_users()

            self.user_combo.set(
                name.strip()
            )

            self.view_history()

            messagebox.showinfo(
                "Success",
                "BMI calculated and saved successfully!"
            )

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )

    # ---------------- COLOUR ----------------

    def set_category_colour(
        self,
        category
    ):

        colours = {
            "Underweight": "blue",
            "Normal": "green",
            "Overweight": "orange",
            "Obese": "red"
        }

        self.category_label.config(
            foreground=colours.get(
                category,
                "black"
            )
        )

    # ---------------- USERS ----------------

    def refresh_users(self):

        users = get_users()

        self.user_combo["values"] = users

        if users:

            if not self.user_combo.get():

                self.user_combo.set(
                    users[0]
                )

    # ---------------- HISTORY ----------------

    def view_history(self):

        user_name = self.user_combo.get()

        if not user_name:

            messagebox.showwarning(
                "No User",
                "Please select a user."
            )

            return

        for item in self.tree.get_children():

            self.tree.delete(item)

        records = get_user_records(
            user_name
        )

        for record in records:

            date_time = record[0]
            weight = record[1]
            height = record[2]
            bmi = record[3]
            category = record[4]

            self.tree.insert(
                "",
                "end",
                values=(
                    date_time,
                    f"{weight:.2f}",
                    f"{height:.2f}",
                    f"{bmi:.2f}",
                    category
                )
            )

    # ---------------- TREND GRAPH ----------------

    def show_trend(self):

        user_name = self.user_combo.get()

        if not user_name:

            messagebox.showwarning(
                "No User",
                "Please select a user."
            )

            return

        records = get_user_records(
            user_name
        )

        if not records:

            messagebox.showinfo(
                "No Data",
                "No BMI records found."
            )

            return

        records.reverse()

        dates = [
            record[0]
            for record in records
        ]

        bmi_values = [
            record[3]
            for record in records
        ]

        plt.figure(
            figsize=(10, 5)
        )

        plt.plot(
            dates,
            bmi_values,
            marker="o"
        )

        plt.title(
            f"BMI Trend - {user_name}"
        )

        plt.xlabel(
            "Date and Time"
        )

        plt.ylabel(
            "BMI"
        )

        plt.xticks(
            rotation=45
        )

        plt.grid(
            True
        )

        plt.tight_layout()

        plt.show()