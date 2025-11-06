import tkinter as tk
from quiz_gui import QuizGUI


def main():
    root = tk.Tk()
    app = QuizGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
