from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# =========================
# LOAD DATA
# =========================

BASE_DIR = Path(__file__).resolve().parents[2]

CSV_PATH = BASE_DIR / "output" / "utility_problems.csv"

df = pd.read_csv(CSV_PATH)


# =========================
# BASIC ANALYSIS
# =========================

print("\n=== DATASET OVERVIEW ===")

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# =========================
# INDUSTRIES
# =========================

print("\n=== INDUSTRIES ===")

print(df["industry"].value_counts())


# =========================
# PROBLEM CATEGORIES
# =========================

print("\n=== PROBLEM CATEGORIES ===")

print(df["problem_category"].value_counts())


# =========================
# TOP 20 PROBLEMS
# =========================

print("\n=== TOP 20 PROBLEMS ===")

print(df["problem"].value_counts().head(20))


# =========================
# TOP 20 PROJECTS
# =========================

print("\n=== TOP 20 PROJECTS ===")

print(df["project"].value_counts().head(20))


# =========================
# PROCUREMENT STATUS
# =========================

print("\n=== PROCUREMENT STATUS ===")

print(df["procurement_status"].value_counts())


# =========================
# TOP 20 STATES
# =========================

print("\n=== TOP 20 STATES ===")

top_states = df["state"].value_counts().head(20)

print(top_states)


# =========================
# AVERAGE LEAD SCORE
# =========================

print("\n=== AVERAGE LEAD SCORE BY PROBLEM CATEGORY ===")

print(df.groupby("problem_category")["lead_score"].mean().sort_values(ascending=False))


# =========================
# PROBLEM CATEGORY ANALYSIS
# =========================

print("\n=== PROBLEM CATEGORY ANALYSIS ===")

problem_analysis = (
    df.groupby("problem_category")["lead_score"]
    .agg(count="count", mean="mean", max="max")
    .sort_values("mean", ascending=False)
)

print(problem_analysis)


# =========================
# VALTIREN OPPORTUNITY ANALYSIS
# =========================

print("\n=== VALTIREN OPPORTUNITY ANALYSIS ===")

opportunity_analysis = (
    df.groupby("valtiren_opportunity")
    .agg(
        records=("valtiren_opportunity", "size"),
        average_lead_score=("lead_score", "mean"),
        highest_lead_score=("lead_score", "max"),
    )
    .sort_values("average_lead_score", ascending=False)
)

print(opportunity_analysis)


# =========================
# TOP 50 VALTIREN OPPORTUNITIES
# =========================

print("\n=== TOP 50 VALTIREN OPPORTUNITIES ===")

top_opportunities = df.sort_values("lead_score", ascending=False)[
    [
        "company",
        "industry",
        "state",
        "problem_category",
        "problem",
        "technology",
        "project",
        "valtiren_opportunity",
        "lead_score",
    ]
].head(50)

print(top_opportunities.to_string(index=False))


# =========================================================
# STATE DRILL-DOWN
# =========================================================

print("\n")
print("=" * 80)
print("STATE MARKET INTELLIGENCE")
print("=" * 80)


for state in top_states.index:

    state_df = df[df["state"] == state]

    print("\n")
    print("=" * 80)
    print(f"STATE: {state}")
    print(f"TOTAL RECORDS: {len(state_df)}")
    print("=" * 80)

    # =========================
    # TOP 10 PROBLEMS
    # =========================

    print("\n--- TOP 10 PROBLEMS ---")

    print(state_df["problem"].value_counts().head(10))

    # =========================
    # TOP 10 TECHNOLOGIES
    # =========================

    print("\n--- TOP 10 TECHNOLOGIES ---")

    technology_counts = (
        state_df["technology"]
        .dropna()
        .str.split(";")
        .explode()
        .str.strip()
        .value_counts()
        .head(10)
    )

    print(technology_counts)

    # =========================
    # TOP 10 PROJECTS
    # =========================

    print("\n--- TOP 10 PROJECTS ---")

    print(state_df["project"].value_counts().head(10))

    # =========================
    # TOP 10 VALTIREN OPPORTUNITIES
    # =========================

    print("\n--- TOP 10 VALTIREN OPPORTUNITIES ---")

    print(state_df["valtiren_opportunity"].value_counts().head(10))

    # =========================
    # AVERAGE LEAD SCORE
    # =========================

    print("\n--- AVERAGE LEAD SCORE BY PROBLEM CATEGORY ---")

    state_category_scores = (
        state_df.groupby("problem_category")["lead_score"]
        .mean()
        .sort_values(ascending=False)
    )

    print(state_category_scores)

    # =========================
    # TOP 10 LEAD OPPORTUNITIES
    # =========================

    print("\n--- TOP 10 LEAD OPPORTUNITIES ---")

    top_state_opportunities = state_df.sort_values("lead_score", ascending=False)[
        [
            "company",
            "problem_category",
            "problem",
            "technology",
            "project",
            "valtiren_opportunity",
            "lead_score",
        ]
    ].head(10)

    print(top_state_opportunities.to_string(index=False))


# =========================================================
# VISUALIZATION
# =========================================================


# =========================
# 1. PROBLEM CATEGORIES
# =========================

problem_categories = df["problem_category"].value_counts()

plt.figure(figsize=(10, 6))

problem_categories.plot(kind="bar")

plt.title("Utility Problems by Category")

plt.xlabel("Problem Category")

plt.ylabel("Number of Records")

plt.xticks(rotation=45, ha="right")

plt.tight_layout()

plt.show()


# =========================
# 2. TOP 20 PROBLEMS
# =========================

top_problems = df["problem"].value_counts().head(20)

plt.figure(figsize=(10, 7))

top_problems.sort_values().plot(kind="barh")

plt.title("Top 20 Recurring Utility Problems")

plt.xlabel("Number of Records")

plt.ylabel("Problem")

plt.tight_layout()

plt.show()


# =========================
# 3. TOP 20 STATES
# =========================

plt.figure(figsize=(10, 7))

top_states.sort_values().plot(kind="barh")

plt.title("Top 20 States by Number of Records")

plt.xlabel("Number of Records")

plt.ylabel("State")

plt.tight_layout()

plt.show()


# =========================
# 4. LEAD SCORE BY CATEGORY
# =========================

lead_scores = df.groupby("problem_category")["lead_score"].mean().sort_values()

plt.figure(figsize=(10, 6))

lead_scores.plot(kind="barh")

plt.title("Average Lead Score by Problem Category")

plt.xlabel("Average Lead Score")

plt.ylabel("Problem Category")

plt.tight_layout()

plt.show()


# =========================
# 5. VALTIREN OPPORTUNITY SCORE
# =========================

opportunity_scores = (
    df.groupby("valtiren_opportunity")["lead_score"].mean().sort_values()
)

plt.figure(figsize=(10, 7))

opportunity_scores.plot(kind="barh")

plt.title("Average Lead Score by Valtiren Opportunity")

plt.xlabel("Average Lead Score")

plt.ylabel("Valtiren Opportunity")

plt.tight_layout()

plt.show()


# =========================
# 6. OPPORTUNITY FREQUENCY
# =========================

opportunity_counts = df["valtiren_opportunity"].value_counts().head(20)

plt.figure(figsize=(10, 7))

opportunity_counts.sort_values().plot(kind="barh")

plt.title("Top 20 Valtiren Opportunities by Frequency")

plt.xlabel("Number of Records")

plt.ylabel("Valtiren Opportunity")

plt.tight_layout()

plt.show()


# =========================
# 7. TOP TECHNOLOGIES
# =========================

technology_counts = (
    df["technology"]
    .dropna()
    .str.split(";")
    .explode()
    .str.strip()
    .value_counts()
    .head(20)
)

plt.figure(figsize=(10, 7))

technology_counts.sort_values().plot(kind="barh")

plt.title("Top 20 Technologies in Utility Research")

plt.xlabel("Number of Records")

plt.ylabel("Technology")

plt.tight_layout()

plt.show()
