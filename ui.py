# ui.py

import os
import time
import tkinter as tk
import colorama

from tkinter import messagebox
from tkinter import ttk
from logic import GameLogic
from i18n import Translator

colorama.init(autoreset=True)
tr = Translator(lang_code="ru_RU")

class GameUI:
    def __init__(self, root):
        self.game = GameLogic()
        self.root = root
        self.root.title(tr.__("Guess the number"))
        self.root.geometry("700x520")
        self.show_banner()

        self.label = tk.Label(root, text=tr.__("Guess a number between 1 and 100"), font=("Arial", 14))
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, font=("Arial", 12))
        self.entry.pack()
        self.entry.bind('<Return>', self.on_enter_pressed)

        self.prepare_buttons()

        self.status = tk.Label(root, text=tr.__("You have {} attempts", self.game.max_attempts), font=("Arial", 14))
        self.status.pack()
        self.prepare_table()

    def process_input(self):
        guess_str = self.entry.get()
        self.entry.delete(0, tk.END)

        if not guess_str.isdigit():
            messagebox.showwarning(tr.__("Error"), tr.__("Please enter a number!"))
            return

        guess = int(guess_str)
        result = self.game.check_guess(guess)
        attempt_no = self.game.attempts

        resultText = {
            "<": "Lower",
            ">": "Higher",
            "==": "Victory"
        }.get(result, "???")

        self.results_table.insert("", tk.END, values=(attempt_no, guess, tr.__(resultText)))

        if result == ">" or result == "<":
            self.status.config(
                text=tr.__("{}! Attempts left: {}", tr.__(resultText), self.game.remaining_attempts()),
                font=("Arial", 14)
            )
        elif result == "==":
            messagebox.showinfo(tr.__(resultText) + "!", tr.__("You guessed it in {} attempts!", self.game.attempts))
            self.restart_game()
            return

        if self.game.is_game_over():
            messagebox.showerror(tr.__("Game Over"), tr.__("Number was: {}", self.game.secret))
            self.restart_game()

    def restart_game(self):
        self.game.reset()
        for row in self.results_table.get_children():
            self.results_table.delete(row)
        self.status.config(text=tr.__("You have {} attempts", self.game.max_attempts), font=("Arial", 14))
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
            banner_text = tr.__("Guess the number")

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

        self.check_button = tk.Button(table_frame, text=tr.__("Check"), command=self.process_input)
        self.restart_button = tk.Button(table_frame, text=tr.__("Restart"), command=self.restart_game)

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
            height=9
        )

        for name, width in columns.items():
            self.results_table.heading(name, text=tr.__(name).capitalize())
            self.results_table.column(name, width=width, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.results_table.yview)
        self.results_table.configure(yscrollcommand=scrollbar.set)

        self.results_table.grid(row=0, column=0)
        scrollbar.grid(row=0, column=1, sticky="ns")
