import re
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

from .config import (
    HEADERS,
    REQUEST_TIMEOUT,
    TECHNOLOGY_SIGNALS,
    PROBLEM_SIGNALS,
    OPPORTUNITY_SIGNALS,
    ELECTRIC_CONTEXT_SIGNALS,
)


def download_page(url: str) -> str:
    try:
        response = httpx.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
            follow_redirects=True,
        )

        response.raise_for_status()

        return response.text

    except Exception as exc:
        print(f"  Download failed: {exc}")
        return ""


def extract_text(html: str) -> str:
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

    lower = text.lower()
    found = []

    for category, keywords in signals.items():
        for keyword in keywords:
            if keyword.lower() in lower:
                found.append(category)
                break

    return found


def detect_electric_context(
    text: str,
) -> list[str]:

    lower = text.lower()
    found = []

    for keyword in ELECTRIC_CONTEXT_SIGNALS:
        if keyword.lower() in lower:
            found.append(keyword)

    return list(dict.fromkeys(found))


def extract_phone(text: str) -> str:

    match = re.search(
        r"(?:\+?1[\s.-]?)?" r"\(?\d{3}\)?[\s.-]" r"\d{3}[\s.-]" r"\d{4}",
        text,
    )

    return match.group(0) if match else ""


def extract_email(text: str) -> str:

    match = re.search(
        r"[A-Za-z0-9._%+-]+" r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text,
    )

    return match.group(0) if match else ""


def extract_money(text: str) -> list[str]:

    matches = re.findall(
        r"\$[\d,.]+" r"(?:\s*(?:million|billion|M|B))?",
        text,
        flags=re.IGNORECASE,
    )

    return list(dict.fromkeys(matches))


def extract_employee_count(text: str) -> str:

    patterns = [
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


def extract_customers(text: str) -> str:

    patterns = [
        r"([\d,]+)\s+customers",
        r"serves\s+([\d,]+)",
        r"serving\s+([\d,]+)",
        r"([\d,]+)\s+customers\s+served",
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


def classify_size(employees: str) -> str:

    if not employees:
        return ""

    try:
        count = int(employees.replace(",", ""))

    except ValueError:
        return ""

    if count < 100:
        return "Small"

    if count < 1000:
        return "Medium"

    return "Large"


def get_domain(url: str) -> str:

    if not url:
        return ""

    return urlparse(url).netloc


def build_opportunity(
    row: dict,
    detected_problems: list[str],
    detected_technology: list[str],
    detected_opportunities: list[str],
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
        return "Electric utility GIS modernization " "and Utility Network"

    if "Poor Spatial Data" in detected_problems:
        return "Electric grid GIS and " "asset data modernization"

    if "Grid Asset Management" in detected_technology:
        return "Electric grid asset management " "and GIS"

    if "Predictive Maintenance" in detected_problems:
        return "AI / IoT predictive maintenance " "for grid assets"

    if "Grid IoT" in detected_technology:
        return "IoT grid monitoring " "and asset intelligence"

    if "AI / Machine Learning" in detected_technology:
        return "AI-powered electric grid " "analytics"

    if "Data Integration" in detected_problems:
        return "Electric utility data integration " "and modernization"

    if "Utility Data Platform" in detected_technology:
        return "Electric utility data platform " "and integration"

    if "SCADA" in detected_technology:
        return "SCADA / GIS / grid data integration"

    if "ADMS" in detected_technology:
        return "ADMS / GIS / grid data integration"

    if "Digital Twin" in detected_technology:
        return "Electric grid digital twin"

    if "Drone Inspection" in detected_technology:
        return "AI / GIS electric infrastructure " "inspection"

    if detected_opportunities:
        return "Electric utility technology " "modernization"

    return ""


def calculate_score(
    row: dict,
    problems: list[str],
    technologies: list[str],
    opportunities: list[str],
    money_signals: list[str],
    electric_context: list[str],
) -> int:

    try:
        score = int(
            row.get(
                "lead_score",
                0,
            )
            or 0
        )

    except ValueError, TypeError:
        score = 0

    if electric_context:
        score += 15

    score += min(
        len(problems) * 5,
        25,
    )

    score += min(
        len(technologies) * 3,
        20,
    )

    score += min(
        len(opportunities) * 5,
        15,
    )

    if money_signals:
        score += 10

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


def enrich_record(row: dict) -> dict:

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

    electric_context = detect_electric_context(text)

    problems = detect_signals(
        text,
        PROBLEM_SIGNALS,
    )

    technologies = detect_signals(
        text,
        TECHNOLOGY_SIGNALS,
    )

    opportunities = detect_signals(
        text,
        OPPORTUNITY_SIGNALS,
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
        opportunities,
    )

    score = calculate_score(
        row,
        problems,
        technologies,
        opportunities,
        money_signals,
        electric_context,
    )

    result = {
        **row,
        "website_domain": get_domain(source_url),
        "electric_context": "; ".join(electric_context),
        "employees": employees,
        "customers": customers,
        "size_enriched": size,
        "detected_problems": "; ".join(problems),
        "detected_technology": "; ".join(technologies),
        "detected_opportunities": "; ".join(opportunities),
        "financial_signals": "; ".join(money_signals),
        "phone": phone,
        "email": email,
        "valtiren_opportunity": opportunity,
        "lead_score_enriched": score,
        "source_status": ("scraped" if text else "failed"),
    }

    print(f"  Electric context: " f"{len(electric_context)}")

    print(f"  Problems: {problems}")
    print(f"  Technology: {technologies}")
    print(f"  Opportunities: {opportunities}")
    print(f"  Employees: " f"{employees or 'unknown'}")
    print(f"  Score: {score}")

    return result
