# __init__.py

import csv
import os

class Translator:
    def __init__(self, lang_code="en_EN", path="i18n"):
        self.translations = {}
        self.lang_code = lang_code
        self.path = path
        self.load_translations()

    def load_translations(self):
        file_path = os.path.join(self.path, f"{self.lang_code}.csv")
        try:
            with open(file_path, encoding="utf-8") as f:
                reader = csv.reader(f)
                self.translations = {row[0]: row[1] for row in reader if len(row) == 2}
        except FileNotFoundError:
            print(f"Translation file not found: {file_path}")
            self.translations = {}

    def __(self, text, *args):
        translated = self.translations.get(text, text)
        return translated.format(*args) if args else translated

    def set_language(self, lang_code):
        self.lang_code = lang_code
        self.load_translations()
