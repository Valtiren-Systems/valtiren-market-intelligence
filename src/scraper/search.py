import os
import httpx

from dotenv import load_dotenv

load_dotenv()

SERPER_URL = "https://google.serper.dev/search"

API_KEY = os.getenv("SERPER_API_KEY")


SEARCH_QUERIES = [
    '"electric utility" "RFP" GIS',
    '"electric utility" "RFP" "asset management"',
    '"electric utility" "legacy system"',
    '"electric utility" "GIS modernization"',
    '"municipal utility" "RFP" GIS',
    '"water utility" "RFP" GIS',
    '"water utility" "asset management"',
    '"wastewater utility" "asset management"',
    '"utility" "aging infrastructure" "RFP"',
    '"utility" "data integration" "RFP"',
    '"utility" "IoT" "RFP"',
    '"utility" "predictive maintenance"',
    '"utility" "Utility Network" RFP',
    '"utility" "SCADA" modernization',
    '"utility" "AMI" modernization',
    '"utility" "capital improvement plan"',
]


def search_web(
    query: str,
    num_results: int = 10,
) -> list[dict]:

    if not API_KEY:
        raise RuntimeError("SERPER_API_KEY is missing from .env")

    response = httpx.post(
        SERPER_URL,
        headers={
            "X-API-KEY": API_KEY,
            "Content-Type": "application/json",
        },
        json={
            "q": query,
            "num": num_results,
        },
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    results = []

    for item in data.get(
        "organic",
        [],
    ):

        results.append(
            {
                "title": item.get(
                    "title",
                    "",
                ),
                "url": item.get(
                    "link",
                    "",
                ),
                "snippet": item.get(
                    "snippet",
                    "",
                ),
            }
        )

    return results


def collect_search_results() -> list[dict]:

    all_results = []

    for query in SEARCH_QUERIES:

        print(f"\nSearching: {query}")

        try:

            results = search_web(query)

            for result in results:

                result["search_query"] = query

                all_results.append(result)

        except Exception as exc:

            print(f"Search failed: {exc}")

    # Remove duplicate URLs.
    unique = {}

    for result in all_results:

        url = result["url"]

        if url:
            unique[url] = result

    return list(unique.values())
