import pandas as pd

from pathlib import Path

from .enrich import enrich_record
from .export import export_results

BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_FILE = BASE_DIR / "output" / "utility_problems.csv"
OUTPUT_DIR = BASE_DIR / "output"


def main():

    print("=" * 70)
    print("VALTIREN MARKET INTELLIGENCE")
    print("US UTILITY ENRICHER")
    print("=" * 70)

    print(f"\nInput: {INPUT_FILE}")

    if not INPUT_FILE.exists():

        raise FileNotFoundError(f"\nInput CSV does not exist:\n" f"{INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE).fillna("")

    print(f"Records found: {len(df)}")

    results = []

    for index, row in df.iterrows():

        print(f"\n[{index + 1}/{len(df)}]")

        try:

            result = enrich_record(row.to_dict())

            results.append(result)

        except Exception as exc:

            print(f"  ERROR: {exc}")

            # Keep original record even
            # if enrichment fails.
            results.append(row.to_dict())

    export_results(
        results,
        OUTPUT_DIR,
    )


if __name__ == "__main__":
    main()
