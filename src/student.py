import re

import pandas as pd


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

    def _extract_keywords(self, text: str) -> set:
        """
        Cleans up raw data and returns a set of keywords.
        """
        if pd.isna(text):
            return set()
        text = str(text).lower()
        mots = re.findall(
            r"[a-zàâçéèêëîïôûùüÿñæœ]{3,}", text
        )  #                         ^ we only keep > 3 chars to filter noise
        #                              (useless words like "et", "ou", "de"...)
        return set(mots)

    def __repr__(self):
        type_etu = "Inter" if self.is_international else "Local"
        return f"<Student: {self.name} ({type_etu})>"
