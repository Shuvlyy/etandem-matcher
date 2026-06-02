import argparse

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

def main():
    args = parse_args()

if __name__ == "__main__":
    main()
