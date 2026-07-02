import json
from pathlib import Path


class LanguageManager:
    def __init__(self, lang_dir="lang", default_language="en"):
        self.lang_dir = Path(lang_dir)
        self.default_language = default_language
        self.languages = {}

        self.reload()


    def reload(self):
        self.languages.clear()

        if not self.lang_dir.exists():
            return

        for file in self.lang_dir.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    self.languages[file.stem] = json.load(f)
            except Exception as e:
                print(f"Cannot load language '{file.name}': {e}")


    def available_languages(self):
        return sorted(self.languages.keys())


    def exists(self, language):
        return language in self.languages


    def translate(self, language, key, **kwargs):
        lang = self.languages.get(language)

        if lang is None:
            lang = self.languages.get(self.default_language, {})

        text = lang.get(key)

        if text is None:
            text = self.languages.get(self.default_language, {}).get(key, key)

        return text.format(**kwargs)