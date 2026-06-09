import re
import unicodedata

import pandas as pd

level_dict = {"A1": 1, "A2": 2, "B1": 3, "B2": 4, "C1": 5, "C2": 6}


class Student:
    def __init__(self, row, is_international: bool):
        self.email = row["email"]
        self.surname = row["surname"]
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


def load_students(file_path: str, is_international: bool) -> list[Student]:
    df = pd.read_excel(file_path)

    if is_international:
        col_map = {
            "email": "Adresse e-mail universitaire / University email address:",
            "surname": "Prénom / First name :",
            "name": "NOM DE FAMILLE / LAST NAME:",
            "age": "Age (numbers only):",
            "sector": "Filière d'études/ Field of study:",
            "interests": "Quels sont vos centres d'intérêt ? / What are your hobbies ?",
            "target_language_level": "Niveau de français / Level of French :",
        }
    else:
        col_map = {
            "email": "Email utilisateur",
            "surname": "Prénom utilisateur",
            "name": "Nom utilisateur",
            "age": "Age : ",
            "sector": "Composante / UFR :",
            "interests": "Centres d'intérêt :",
            "target_language_level": "Votre niveau en anglais :",
        }

    students = []
    for _, row in df.iterrows():
        standardized_row = {
            "email": row[col_map["email"]],
            "surname": row[col_map["surname"]],
            "name": row[col_map["name"]],
            "age": row[col_map["age"]],
            "sector": row[col_map["sector"]],
            "interests": row[col_map["interests"]],
            "target_language_level": row[col_map["target_language_level"]],
        }
        print(standardized_row["surname"])
        students.append(Student(standardized_row, is_international=is_international))

    return students
