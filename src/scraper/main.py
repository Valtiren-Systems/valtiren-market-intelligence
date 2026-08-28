from pathlib import Path

from .search import collect_search_results
from .scrape import scrape_page
from .extract import extract_problem
from .export import export_results

BASE_DIR = Path(__file__).resolve().parents[2]

OUTPUT_DIR = BASE_DIR / "output"


def main():

    print("=" * 70)
    print("VALTIREN MARKET INTELLIGENCE")
    print("US UTILITY PROBLEM MINER")
    print("=" * 70)

    # ------------------------------------------------
    # SEARCH
    # ------------------------------------------------

    print("\n[1/3] Searching public web...")

    search_results = collect_search_results()

    print(f"\nFound {len(search_results)} unique URLs.")

    # ------------------------------------------------
    # SCRAPE
    # ------------------------------------------------

    print("\n[2/3] Scraping sources...")

    all_results = []

    for index, result in enumerate(
        search_results,
        start=1,
    ):

        url = result["url"]

        print(f"\n[{index}/{len(search_results)}]")

        print(result["title"])

        print(url)

        page = scrape_page(url)

        if page["status"] != "success":

            print("  Skipped.")

            continue

        problems = extract_problem(
            text=page["text"],
            source_url=url,
            title=result["title"],
        )

        print(f"  Problems found: {len(problems)}")

        all_results.extend(problems)

    # ------------------------------------------------
    # EXPORT
    # ------------------------------------------------

    print("\n[3/3] Exporting...")

    export_results(
        all_results,
        OUTPUT_DIR,
    )

    print("\nFinished.")


if __name__ == "__main__":
    main()
