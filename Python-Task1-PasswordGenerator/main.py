import tkinter as tk

from gui import PasswordGeneratorGUI


def main():
    root = tk.Tk()

    PasswordGeneratorGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()