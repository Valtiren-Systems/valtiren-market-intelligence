import httpx

from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": ("Mozilla/5.0 " "(compatible; ValtirenMarketIntelligence/1.0)")
}


def download_url(
    url: str,
) -> tuple[str, str]:

    response = httpx.get(
        url,
        headers=HEADERS,
        timeout=30,
        follow_redirects=True,
    )

    response.raise_for_status()

    content_type = response.headers.get(
        "content-type",
        "",
    ).lower()

    return (
        response.text,
        content_type,
    )


def extract_html_text(
    html: str,
) -> str:

    soup = BeautifulSoup(
        html,
        "lxml",
    )

    for element in soup(
        [
            "script",
            "style",
            "noscript",
            "svg",
            "nav",
            "footer",
        ]
    ):
        element.decompose()

    text = soup.get_text(
        " ",
        strip=True,
    )

    return " ".join(text.split())


def scrape_page(
    url: str,
) -> dict:

    try:

        html, content_type = download_url(url)

        if "text/html" not in content_type:

            return {
                "url": url,
                "text": "",
                "type": "unsupported",
                "status": "skipped",
            }

        text = extract_html_text(html)

        return {
            "url": url,
            "text": text,
            "type": "html",
            "status": "success",
        }

    except Exception as exc:

        return {
            "url": url,
            "text": "",
            "type": "error",
            "status": str(exc),
        }
