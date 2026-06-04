import re
import unicodedata

import pandas as pd

level_dict = {"A1": 1, "A2": 2, "B1": 3, "B2": 4, "C1": 5, "C2": 6}


class Student:
    def __init__(self, row, is_international: bool):
        self.email = row["email"]
        self.name = row["name"]
        self.age = row["age"]
        self.is_international = is_international

        self.raw_sector = row["sector"]
        self.raw_interests = row["interests"]

        self.interests = self._extract_keywords(self.raw_interests)
        self.sector = self._extract_keywords(self.raw_sector)

        self.target_language_level = row["target_language_level"]  # level_dict.get(, 2)

    def _extract_keywords(self, text: str) -> set:
        """
        Cleans up raw data and returns a set of keywords.
        """
        if pd.isna(text):
            return set()

        text = str(text).lower()
        text = "".join(
            c
            for c in unicodedata.normalize("NFD", text)
            if unicodedata.category(c) != "Mn"
        )
        mots = re.findall(
            r"[a-z]{3,}", text
        )  #        ^ we only keep > 3 chars to filter noise
        #             (useless words like "et", "ou", "de"...)
        return set(mots)

    def __repr__(self):
        type_etu = "Inter" if self.is_international else "Local"
        return f"<Student: {self.name} ({type_etu})>"
