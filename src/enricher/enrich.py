import re
import httpx

from urllib.parse import urlparse
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": ("Mozilla/5.0 " "(compatible; ValtirenMarketIntelligence/1.0)")
}


TECHNOLOGY_SIGNALS = {
    "GIS": [
        "gis",
        "geographic information system",
        "geospatial",
    ],
    "Utility Network": [
        "utility network",
        "arcgis utility network",
        "esri utility network",
    ],
    "SCADA": [
        "scada",
    ],
    "AMI": [
        "advanced metering infrastructure",
        "ami",
    ],
    "IoT": [
        "internet of things",
        "iot",
    ],
    "AI": [
        "artificial intelligence",
        "machine learning",
        "predictive analytics",
    ],
    "Cloud": [
        "cloud migration",
        "cloud platform",
        "cloud infrastructure",
    ],
    "Asset Management": [
        "asset management",
        "asset inventory",
    ],
}


PROBLEM_SIGNALS = {
    "Aging Infrastructure": [
        "aging infrastructure",
        "ageing infrastructure",
        "aging assets",
        "aging equipment",
    ],
    "Legacy Systems": [
        "legacy system",
        "legacy systems",
        "outdated system",
        "obsolete system",
    ],
    "Data Integration": [
        "data integration",
        "system integration",
        "data silos",
        "siloed data",
    ],
    "Data Quality": [
        "data quality",
        "inaccurate data",
        "incomplete data",
        "inconsistent data",
    ],
    "Manual Processes": [
        "manual process",
        "manual processes",
        "paper-based",
        "manual data entry",
    ],
    "GIS Modernization": [
        "gis modernization",
        "gis migration",
        "gis replacement",
        "utility network migration",
    ],
    "Asset Management": [
        "asset management",
        "asset inventory",
        "asset tracking",
    ],
    "Predictive Maintenance": [
        "predictive maintenance",
        "condition monitoring",
        "predictive analytics",
    ],
    "Remote Monitoring": [
        "remote monitoring",
        "remote sensing",
        "real-time monitoring",
    ],
    "Infrastructure Modernization": [
        "infrastructure modernization",
        "infrastructure upgrade",
        "system modernization",
    ],
}


def download_page(url: str) -> str:
    """Download an existing source URL."""

    try:
        response = httpx.get(
            url,
            headers=HEADERS,
            timeout=30,
            follow_redirects=True,
        )

        response.raise_for_status()

        return response.text

    except Exception as exc:

        print(f"  Download failed: {exc}")

        return ""


def extract_text(html: str) -> str:
    """Convert HTML into readable text."""

    if not html:
        return ""

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
        ]
    ):
        element.decompose()

    return " ".join(
        soup.get_text(
            " ",
            strip=True,
        ).split()
    )


def detect_signals(
    text: str,
    signals: dict[str, list[str]],
) -> list[str]:
    """Detect known signals in source text."""

    lower = text.lower()

    found = []

    for category, keywords in signals.items():

        for keyword in keywords:

            if keyword.lower() in lower:

                found.append(category)

                break

    return found


def extract_phone(
    text: str,
) -> str:

    match = re.search(
        r"(?:\+?1[\s.-]?)?" r"\(?\d{3}\)?[\s.-]" r"\d{3}[\s.-]\d{4}",
        text,
    )

    return match.group(0) if match else ""


def extract_email(
    text: str,
) -> str:

    match = re.search(
        r"[A-Za-z0-9._%+-]+" r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text,
    )

    return match.group(0) if match else ""


def extract_money(
    text: str,
) -> list[str]:

    matches = re.findall(
        r"\$[\d,.]+" r"(?:\s*(?:million|billion|M|B))?",
        text,
        flags=re.IGNORECASE,
    )

    return list(dict.fromkeys(matches))


def extract_employee_count(
    text: str,
) -> str:

    patterns = [
        r"([\d,]+)\s+employees",
        r"([\d,]+)\s+employees",
        r"workforce\s+of\s+([\d,]+)",
        r"employs\s+([\d,]+)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match:
            return match.group(1)

    return ""


def extract_customers(
    text: str,
) -> str:

    patterns = [
        r"([\d,]+)\s+customers",
        r"serves\s+([\d,]+)",
        r"serving\s+([\d,]+)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match:
            return match.group(1)

    return ""


def classify_size(
    employees: str,
) -> str:

    if not employees:
        return ""

    try:

        count = int(
            employees.replace(
                ",",
                "",
            )
        )

    except ValueError:

        return ""

    if count < 100:
        return "Small"

    if count < 1000:
        return "Medium"

    return "Large"


def get_domain(
    url: str,
) -> str:

    if not url:
        return ""

    return urlparse(url).netloc


def build_opportunity(
    row: dict,
    detected_problems: list[str],
    detected_technology: list[str],
) -> str:

    existing = str(
        row.get(
            "valtiren_opportunity",
            "",
        )
    ).strip()

    if existing:
        return existing

    if "GIS Modernization" in detected_problems:
        return "GIS modernization / " "utility network migration"

    if "Asset Management" in detected_problems:
        return "Utility asset management " "and GIS"

    if "Predictive Maintenance" in detected_problems:
        return "IoT / predictive " "maintenance"

    if "Data Integration" in detected_problems:
        return "Utility data integration " "and modernization"

    if detected_technology:
        return "Utility technology " "modernization"

    return ""


def calculate_score(
    row: dict,
    problems: list[str],
    technologies: list[str],
    money_signals: list[str],
) -> int:

    try:

        score = int(
            row.get(
                "lead_score",
                0,
            )
            or 0
        )

    except ValueError:

        score = 0

    # Strong problem evidence.
    score += min(
        len(problems) * 5,
        20,
    )

    # Technology signals.
    score += min(
        len(technologies) * 3,
        15,
    )

    # Financial signal.
    if money_signals:
        score += 10

    # Procurement signal.
    procurement = str(
        row.get(
            "procurement_status",
            "",
        )
    ).lower()

    if any(
        word in procurement
        for word in [
            "rfp",
            "rfq",
            "bid",
            "solicitation",
        ]
    ):
        score += 10

    return min(
        score,
        100,
    )


def enrich_record(
    row: dict,
) -> dict:

    company = str(
        row.get(
            "company",
            "",
        )
    ).strip()

    source_url = str(
        row.get(
            "source_url",
            "",
        )
    ).strip()

    print(f"\nEnriching: {company}")
    print(f"Source: {source_url}")

    html = download_page(source_url)
    text = extract_text(html)
    problems = detect_signals(
        text,
        PROBLEM_SIGNALS,
    )

    technologies = detect_signals(
        text,
        TECHNOLOGY_SIGNALS,
    )

    employees = extract_employee_count(text)
    customers = extract_customers(text)
    money_signals = extract_money(text)
    phone = extract_phone(text)
    email = extract_email(text)
    size = classify_size(employees)
    opportunity = build_opportunity(
        row,
        problems,
        technologies,
    )
    score = calculate_score(
        row,
        problems,
        technologies,
        money_signals,
    )
    result = {
        **row,
        "website_domain": get_domain(source_url),
        "employees": employees,
        "customers": customers,
        "size_enriched": size,
        "detected_problems": ("; ".join(problems)),
        "detected_technology": ("; ".join(technologies)),
        "financial_signals": ("; ".join(money_signals)),
        "phone": phone,
        "email": email,
        "valtiren_opportunity": opportunity,
        "lead_score_enriched": score,
        "source_status": ("scraped" if text else "failed"),
    }

    print(f"  Problems: {problems}")
    print(f"  Technology: {technologies}")
    print(f"  Employees: {employees or 'unknown'}")
    print(f"  Score: {score}")

    return result
