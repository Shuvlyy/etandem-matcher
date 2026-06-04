import argparse


def parse_arguments() -> argparse.Namespace:
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
        default="results.xlsx",
        help="Output Excel file name",
    )
    return parser.parse_args()
