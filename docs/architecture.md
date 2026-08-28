# Architecture

## Tech Stack

1. **Python 3.14**
2. **uv (Astral)** — package and environment management
3. **Serper API** — web search and discovery
4. **pandas** — structured data processing
5. **Pydantic** — data validation and schemas
6. **CSV** — lightweight data storage/export
7. **httpx** — HTTP client
8. **BeautifulSoup** — HTML parsing
9. **python-dotenv** — environment configuration

## Overview

```text
                    Valtiren Problem Miner
                             │
              ┌──────────────┼──────────────┐
              ↓              ↓              ↓
        EIA / EPA        Google/Search   Utility
        Structured        Discovery      Websites
              │              │              │
              └──────────────┼──────────────┘
                             ↓
                    Candidate Utilities
                             ↓
                      Website Crawler
                             ↓
                  Relevant Pages + PDFs
                             ↓
                    Problem Extraction
                             ↓
                     Evidence + Source
                             ↓
                     Problem Scoring
                             ↓
                 MCP AI Data Enhancement
                             ↓
                    Lead / Opportunity
```

### Pipeline

The system follows a pipeline that moves from **utility discovery → website crawling → problem identification → evidence collection → scoring → AI enrichment → lead generation**.

Each stage produces structured data that can be passed to the next stage, keeping discovery, scraping, extraction, and enrichment separated.

## App Structure

```text
src/
├── enricher/
├── scraper/
├── mcp_server/
└── output/
```

### Components

* **`enricher/`** — Processes and enhances extracted utility/problem data.
* **`scraper/`** — Handles search results, website crawling, page parsing, and document discovery.
* **`mcp_server/`** — Exposes structured data and AI-enhancement capabilities through MCP.
* **`output/`** — Stores or exports final datasets, reports, and lead opportunities.
