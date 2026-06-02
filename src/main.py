import argparse

import pandas as pd

from matcher import Matcher
from student import Student


def parse_args():
    parser = argparse.ArgumentParser(description="E-Tandem Matcher Algorithm")

    parser.add_argument(
        "--interxl",
        type=str,
        default="etudiants_internationaux_test.xlsx",
        help="Path to the International Students Excel file",
    )
    parser.add_argument(
        "--localxl",
        type=str,
        default="etudiants_locaux_test.xlsx",
        help="Path to the Local Students Excel file",
    )
    return parser.parse_args()


def load_students(file_path: str, is_international: bool) -> list[Student]:
    df = pd.read_excel(file_path)

    if is_international:
        col_map = {
            "email": "Adresse e-mail universitaire / University email address:",
            "name": "Prénom / First name :",
            "age": "Age (numbers only):",
            "sector": "Filière d'études/ Field of study:",
            "interests": "Quels sont vos centres d'intérêt ? / What are your hobbies ?",
        }
    else:
        col_map = {
            "email": "Email utilisateur",
            "name": "Prénom utilisateur",
            "age": "Age : ",
            "sector": "Composante / UFR :",
            "interests": "Centres d'intérêt :",
        }

    students = []
    for _, row in df.iterrows():
        standardized_row = {
            "email": row[col_map["email"]],
            "name": row[col_map["name"]],
            "age": row[col_map["age"]],
            "sector": row[col_map["sector"]],
            "interests": row[col_map["interests"]],
        }
        students.append(Student(standardized_row, is_international=is_international))

    return students


def main():
    args = parse_args()

    list_internationals = load_students(args.interxl, is_international=True)
    list_locals = load_students(args.localxl, is_international=False)

    print(
        f"Successfully loaded {len(list_internationals)} international and {len(list_locals)} local students.\n"
    )

    matcher = Matcher(list_internationals, list_locals)
    matrice = matcher.build_score_matrix()

    print("--- Score Matrix ---")
    print(matrice)


if __name__ == "__main__":
    main()
