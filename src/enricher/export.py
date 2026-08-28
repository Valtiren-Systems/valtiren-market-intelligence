import json
import pandas as pd

from pathlib import Path



def export_results(
    results: list[dict],
    output_dir: Path,
) -> None:

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    df = pd.DataFrame(results)

    csv_path = output_dir / "enriched_utilities.csv"

    json_path = output_dir / "enriched_utilities.json"

    df.to_csv(
        csv_path,
        index=False,
    )

    with open(
        json_path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print()
    print("=" * 70)
    print("ENRICHMENT COMPLETE")
    print("=" * 70)

    print(f"CSV:     {csv_path}")

    print(f"JSON:    {json_path}")

    print(f"Records: {len(results)}")
