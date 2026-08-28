import pandas as pd

from pathlib import Path
from mcp.server.mcpserver import MCPServer

BASE_DIR = Path(__file__).resolve().parents[2]
CSV_FILE = BASE_DIR / "output" / "enriched_utilities.csv"


mcp = MCPServer("Valtiren Market Intelligence")


def load_data() -> pd.DataFrame:

    if not CSV_FILE.exists():

        raise FileNotFoundError(f"Missing data file:\n{CSV_FILE}")

    return pd.read_csv(CSV_FILE).fillna("")


@mcp.tool()
def search_leads(
    query: str = "",
    state: str = "",
    technology: str = "",
    problem: str = "",
    min_score: int = 0,
    limit: int = 20,
) -> list[dict]:
    """
    Search Valtiren utility intelligence.

    Searches company, problems, technologies,
    opportunities and other available fields.
    """

    df = load_data()

    # -----------------------------------------
    # General search
    # -----------------------------------------

    if query:

        mask = (
            df.astype(str)
            .apply(
                lambda column: column.str.contains(
                    query,
                    case=False,
                    na=False,
                )
            )
            .any(axis=1)
        )

        df = df[mask]

    # -----------------------------------------
    # State
    # -----------------------------------------

    if state:

        df = df[
            df["state"]
            .astype(str)
            .str.contains(
                state,
                case=False,
                na=False,
            )
        ]

    # -----------------------------------------
    # Technology
    # -----------------------------------------

    if technology:

        technology_mask = (
            df.astype(str)
            .apply(
                lambda column: column.str.contains(
                    technology,
                    case=False,
                    na=False,
                )
            )
            .any(axis=1)
        )

        df = df[technology_mask]

    # -----------------------------------------
    # Problem
    # -----------------------------------------

    if problem:

        problem_mask = (
            df.astype(str)
            .apply(
                lambda column: column.str.contains(
                    problem,
                    case=False,
                    na=False,
                )
            )
            .any(axis=1)
        )

        df = df[problem_mask]

    # -----------------------------------------
    # Lead score
    # -----------------------------------------

    if "lead_score_enriched" in df:

        scores = pd.to_numeric(
            df["lead_score_enriched"],
            errors="coerce",
        ).fillna(0)

        df = df[scores >= min_score]

        df = (
            df.assign(_score=scores)
            .sort_values(
                "_score",
                ascending=False,
            )
            .drop(columns="_score")
        )

    return df.head(limit).to_dict(orient="records")


@mcp.tool()
def get_lead(
    company: str,
) -> list[dict]:
    """
    Get all available intelligence about
    a specific utility/company.
    """

    df = load_data()

    mask = (
        df["company"]
        .astype(str)
        .str.contains(
            company,
            case=False,
            na=False,
        )
    )

    return df[mask].to_dict(orient="records")


@mcp.tool()
def get_top_leads(
    limit: int = 20,
) -> list[dict]:
    """
    Return the highest-scoring leads.
    """

    df = load_data()

    if "lead_score_enriched" not in df:
        return []

    df["lead_score_enriched"] = pd.to_numeric(
        df["lead_score_enriched"],
        errors="coerce",
    ).fillna(0)

    df = df.sort_values(
        "lead_score_enriched",
        ascending=False,
    )

    return df.head(limit).to_dict(orient="records")


@mcp.tool()
def market_summary() -> dict:
    """
    Summarize the current utility market
    intelligence dataset.
    """

    df = load_data()

    result = {
        "records": len(df),
        "companies": (df["company"].nunique() if "company" in df else 0),
    }

    if "state" in df:

        result["states"] = df["state"].value_counts().head(20).to_dict()

    if "problem_category" in df:

        result["problem_categories"] = (
            df["problem_category"].value_counts().head(20).to_dict()
        )

    if "detected_problems" in df:

        result["detected_problems"] = (
            df["detected_problems"]
            .astype(str)
            .str.split("; ")
            .explode()
            .value_counts()
            .head(20)
            .to_dict()
        )

    if "detected_technology" in df:

        result["technologies"] = (
            df["detected_technology"]
            .astype(str)
            .str.split("; ")
            .explode()
            .value_counts()
            .head(20)
            .to_dict()
        )

    return result


if __name__ == "__main__":
    mcp.run()
