# ui.py

import os
import time
import tkinter as tk
import colorama

from tkinter import messagebox
from tkinter import ttk
from logic import GameLogic

colorama.init(autoreset=True)

class GameUI:
    def __init__(self, root):
        self.game = GameLogic()
        self.root = root
        self.root.title("Угадай число")
        self.root.geometry("700x520")
        self.show_banner()

        self.label = tk.Label(root, text="Угадай число от 1 до 100", font=("Arial", 14))
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, font=("Arial", 12))
        self.entry.pack()
        self.entry.bind('<Return>', self.on_enter_pressed)

        self.prepare_buttons()

        self.status = tk.Label(root, text="У тебя 10 попыток", font=("Arial", 14))
        self.status.pack()
        self.prepare_table()

    def process_input(self):
        guess_str = self.entry.get()
        self.entry.delete(0, tk.END)

        if not guess_str.isdigit():
            messagebox.showwarning("Ошибка", "Введите число!")
            return

        guess = int(guess_str)
        result = self.game.check_guess(guess)
        attempt_no = self.game.attempts

        resultText = {
            "<": "Меньше",
            ">": "Больше",
            "==": "Угадал"
        }.get(result, "???")

        self.results_table.insert("", tk.END, values=(attempt_no, guess, resultText))

        if result == ">":
            self.status.config(
                text=f"Больше! Осталось: {self.game.remaining_attempts()}",
                font=("Arial", 14)
            )
        elif result == "<":
            self.status.config(
                text=f"Меньше! Осталось: {self.game.remaining_attempts()}",
                font=("Arial", 14)
            )
        elif result == "==":
            messagebox.showinfo("Победа!", f"Ты угадал за {self.game.attempts} попыток!")
            self.restart_game()
            return

        if self.game.is_game_over():
            messagebox.showerror("Проигрыш", f"Число было: {self.game.secret}")
            self.restart_game()

    def restart_game(self):
        self.game.reset()
        for row in self.results_table.get_children():
            self.results_table.delete(row)
        self.status.config(text="У тебя 10 попыток", font=("Arial", 14))
        self.entry.delete(0, tk.END)
        self.entry.focus()

    def on_enter_pressed(self, event=None):
        self.process_input()

    def show_banner(self, filename="banner.txt", delay=0.003, color = colorama.Fore.CYAN):
        filepath = os.path.join(os.path.dirname(__file__), "header", filename)
        try:
            with open(filepath, encoding="utf-8") as file:
                 banner_text = file.read()
        except FileNotFoundError:
            banner_text = "Угадай число"

        text_widget = tk.Text(
            self.root,
            height=8,
            borderwidth=0,
            font=("Courier New", 10),
            bg=self.root["bg"],
            fg="red"
        )
        text_widget.insert("1.0", banner_text)
        text_widget.config(state="disabled")
        text_widget.pack(pady=(10, 15))

    def prepare_buttons(self):
        table_frame = tk.Frame(self.root)
        table_frame.pack(pady=10, anchor="center")

        self.check_button = tk.Button(table_frame, text="Проверить", command=self.process_input)
        self.restart_button = tk.Button(table_frame, text="Заново", command=self.restart_game)

        self.check_button.grid(row=0, column=0)
        self.restart_button.grid(row=0, column=1)

    def prepare_table(self):
        table_frame = tk.Frame(self.root)
        table_frame.pack(pady=10, anchor="center")

        columns = {
            "№": 30,
            "attempts": 80,
            "result": 100
        }

        self.results_table = ttk.Treeview(
            table_frame,
            columns=list(columns),
            show="headings",
            height=3
        )

        for name, width in columns.items():
            self.results_table.heading(name, text=name.capitalize())
            self.results_table.column(name, width=width, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.results_table.yview)
        self.results_table.configure(yscrollcommand=scrollbar.set)

        self.results_table.grid(row=0, column=0)
        scrollbar.grid(row=0, column=1, sticky="ns")
