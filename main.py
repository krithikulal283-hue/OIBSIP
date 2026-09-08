import tkinter as tk

from database import create_database
from gui import BMICalculatorGUI


def main():

    create_database()

    root = tk.Tk()

    BMICalculatorGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()