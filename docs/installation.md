# Getting Started

## Pre requisite

1. Python 3.14
2. UV Astral
3. Serper for Google Searcher

## Next Steps

1. Prepare .env file to store your serper api key. This removes random search and increase factual ones

```shell
touch .env 
```

```shell
SERPER_API_KEY=your_serper_key
```

2. Install python libraries dependencies

```shell
uv sync
```

## Commands

Most of the command came from python uv run, then stored in [Makefile](../Makefile). You can run them using this below

```shell
make scrape    -> scraping problems and datas
make enrich    -> enriching data with more data
make dev       -> mcp testing
make claude    -> add plugin to claude
```