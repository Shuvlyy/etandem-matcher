import argparse

import pandas as pd

from exporter import export_results_to_excel
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
    parser.add_argument(
        "--topn",
        type=int,
        default=3,
        help="Number of top matches to display",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="resultats.xlsx",
        help="Output Excel file name",
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
    df_top_matches = matcher.get_top_matches(top_n=args.topn)

    print("\n--- Results ---")
    print(df_top_matches.to_string(index=False))

    export_results_to_excel(df_top_matches, filename=args.output)


if __name__ == "__main__":
    main()
