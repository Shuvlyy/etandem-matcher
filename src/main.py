from exporter import export_results_to_excel
from matcher import Matcher
from parser import parse_arguments
from student import load_students


def main():
    args = parse_arguments()

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
