# logic.py

import random

class GameLogic:
    def __init__(self, max_attempts=10):
        self.max_attempts = max_attempts
        self.reset()

    def reset(self):
        self.secret = random.randint(1, 100)
        self.attempts = 0
        self.finished = False

    def check_guess(self, guess):
        if self.finished:
            return "Игра уже завершена."

        self.attempts += 1

        if guess < self.secret:
            return ">"
        elif guess > self.secret:
            return "<"
        else:
            self.finished = True
            return "=="

    def remaining_attempts(self):
        return self.max_attempts - self.attempts

    def is_game_over(self):
        return self.attempts >= self.max_attempts or self.finished
