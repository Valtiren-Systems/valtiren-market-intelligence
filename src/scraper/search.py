import httpx

from .config import (
    API_KEY,
    SERPER_URL,
    SEARCH_QUERIES,
    NUM_RESULTS_PER_QUERY,
    REQUEST_TIMEOUT,
    DEDUPLICATE_RESULTS,
)


def search_web(
    query: str,
    num_results: int = NUM_RESULTS_PER_QUERY,
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
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    data = response.json()

    results = []

    for item in data.get("organic", []):
        results.append(
            {
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "snippet": item.get("snippet", ""),
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

    if not DEDUPLICATE_RESULTS:
        return all_results

    # Remove duplicate URLs.
    unique = {}

    for result in all_results:
        url = result["url"]

        if url:
            unique[url] = result

    return list(unique.values())
