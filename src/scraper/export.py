
import json
import pandas as pd

from pathlib import Path

from .extract import UtilityProblem


def export_results(
    results: list[UtilityProblem],
    output_dir: Path,
) -> None:

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    records = [result.model_dump() for result in results]

    # JSON
    json_path = output_dir / "utility_problems.json"

    with open(
        json_path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            records,
            file,
            indent=2,
            ensure_ascii=False,
        )

    # CSV
    csv_path = output_dir / "utility_problems.csv"

    df = pd.DataFrame(records)

    df.to_csv(
        csv_path,
        index=False,
    )

    print(f"\nCSV: {csv_path}")

    print(f"JSON: {json_path}")

    print(f"Records: {len(records)}")
