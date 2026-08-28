import re

from pydantic import BaseModel


class UtilityProblem(BaseModel):

    company: str = ""
    industry: str = ""
    size: str = ""
    city: str = ""
    state: str = ""
    problem_category: str = ""
    problem: str = ""
    technology: str = ""
    project: str = ""
    procurement_status: str = ""
    revenue: str = ""
    estimated_expense: str = ""
    evidence: str = ""
    source_url: str = ""
    valtiren_opportunity: str = ""
    lead_score: int = 0


PROBLEM_PATTERNS = {
    "GIS": [
        "legacy gis",
        "gis modernization",
        "gis migration",
        "gis conversion",
        "geospatial data",
        "spatial data",
        "outdated mapping",
        "utility network",
        "asset mapping",
    ],
    "Asset Management": [
        "asset management",
        "asset inventory",
        "asset condition",
        "asset inspection",
        "aging assets",
        "infrastructure inventory",
    ],
    "AI": [
        "artificial intelligence",
        "machine learning",
        "predictive analytics",
        "predictive maintenance",
        "anomaly detection",
    ],
    "IoT": [
        "internet of things",
        "iot",
        "smart sensor",
        "remote monitoring",
        "telemetry",
        "condition monitoring",
    ],
    "Data": [
        "data quality",
        "data integration",
        "data migration",
        "data silos",
        "data governance",
        "data standardization",
    ],
    "Infrastructure": [
        "aging infrastructure",
        "infrastructure replacement",
        "infrastructure condition",
        "capacity constraints",
        "aging distribution",
        "equipment replacement",
    ],
    "System Modernization": [
        "legacy system",
        "system modernization",
        "system replacement",
        "digital transformation",
        "cloud migration",
        "technology modernization",
    ],
    "Field Operations": [
        "field data collection",
        "field inspection",
        "mobile workforce",
        "mobile gis",
        "manual process",
        "paper-based",
    ],
    "Grid": [
        "grid modernization",
        "distribution modernization",
        "outage management",
        "load forecasting",
        "distribution planning",
        "scada",
        "adms",
        "oms",
        "ami",
    ],
}


TECHNOLOGY_PATTERNS = [
    "GIS",
    "Esri",
    "ArcGIS",
    "Utility Network",
    "SCADA",
    "ADMS",
    "OMS",
    "AMI",
    "IoT",
    "AWS",
    "Azure",
    "cloud",
    "ERP",
]


PROCUREMENT_PATTERNS = [
    "request for proposal",
    "request for qualifications",
    "RFP",
    "RFQ",
    "procurement",
    "solicitation",
    "bid",
]


def find_matches(
    text: str,
) -> list[dict]:

    lower = text.lower()

    matches = []

    for category, patterns in PROBLEM_PATTERNS.items():

        for pattern in patterns:

            position = lower.find(pattern.lower())

            if position == -1:
                continue

            start = max(
                0,
                position - 300,
            )

            end = min(
                len(text),
                position + len(pattern) + 500,
            )

            evidence = text[start:end]

            matches.append(
                {
                    "category": category,
                    "keyword": pattern,
                    "evidence": evidence,
                }
            )

    return matches


def find_technology(
    text: str,
) -> list[str]:

    lower = text.lower()

    technologies = []

    for technology in TECHNOLOGY_PATTERNS:

        if technology.lower() in lower:

            technologies.append(technology)

    return technologies


def find_procurement_status(
    text: str,
) -> str:

    lower = text.lower()

    if "request for proposal" in lower or "rfp" in lower:
        return "RFP"

    if "request for qualifications" in lower or "rfq" in lower:
        return "RFQ"

    if "procurement" in lower or "solicitation" in lower:
        return "Procurement"

    if "bid" in lower:
        return "Bid"

    return ""


def extract_location(
    text: str,
) -> tuple[str, str]:

    # Basic US state detection.
    states = [
        "Alabama",
        "Alaska",
        "Arizona",
        "Arkansas",
        "California",
        "Colorado",
        "Connecticut",
        "Delaware",
        "Florida",
        "Georgia",
        "Hawaii",
        "Idaho",
        "Illinois",
        "Indiana",
        "Iowa",
        "Kansas",
        "Kentucky",
        "Louisiana",
        "Maine",
        "Maryland",
        "Massachusetts",
        "Michigan",
        "Minnesota",
        "Mississippi",
        "Missouri",
        "Montana",
        "Nebraska",
        "Nevada",
        "New Hampshire",
        "New Jersey",
        "New Mexico",
        "New York",
        "North Carolina",
        "North Dakota",
        "Ohio",
        "Oklahoma",
        "Oregon",
        "Pennsylvania",
        "Rhode Island",
        "South Carolina",
        "South Dakota",
        "Tennessee",
        "Texas",
        "Utah",
        "Vermont",
        "Virginia",
        "Washington",
        "West Virginia",
        "Wisconsin",
        "Wyoming",
    ]

    for state in states:

        if re.search(
            rf"\b{re.escape(state)}\b",
            text,
            re.IGNORECASE,
        ):
            return "", state

    return "", ""


def calculate_score(
    matches: list[dict],
    procurement_status: str,
) -> int:

    categories = {match["category"] for match in matches}

    score = len(categories) * 10

    if procurement_status:
        score += 25

    if "GIS" in categories:
        score += 15

    if "Asset Management" in categories:
        score += 15

    if "Infrastructure" in categories:
        score += 10

    if "System Modernization" in categories:
        score += 10

    return min(
        score,
        100,
    )


def extract_problem(
    text: str,
    source_url: str,
    title: str = "",
) -> list[UtilityProblem]:

    matches = find_matches(text)

    if not matches:
        return []

    technologies = find_technology(text)
    procurement = find_procurement_status(text)
    city, state = extract_location(text)

    score = calculate_score(
        matches,
        procurement,
    )

    results = []

    # Create one record per distinct problem category.
    seen_categories = set()

    for match in matches:

        category = match["category"]

        if category in seen_categories:
            continue

        seen_categories.add(category)

        opportunity_map = {
            "GIS": "GIS modernization / migration",
            "Asset Management": "Asset inventory / management",
            "AI": "AI / predictive analytics",
            "IoT": "IoT / remote monitoring",
            "Data": "Data integration / modernization",
            "Infrastructure": "Infrastructure intelligence",
            "System Modernization": "Legacy system modernization",
            "Field Operations": "Field data / mobile GIS",
            "Grid": "Grid technology / analytics",
        }

        result = UtilityProblem(
            company=title,
            industry="Utilities",
            city=city,
            state=state,
            problem_category=category,
            problem=match["keyword"],
            technology="; ".join(technologies),
            procurement_status=procurement,
            evidence=match["evidence"],
            source_url=source_url,
            valtiren_opportunity=opportunity_map.get(
                category,
                "",
            ),
            lead_score=score,
        )

        results.append(result)

    return results
