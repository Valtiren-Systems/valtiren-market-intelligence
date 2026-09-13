# Getting Started

## Pre requisite

1. Python 3.14
2. UV Astral
3. Serper for Google Searcher
4. Pandas
5. Mathplot lib

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


3. How to use
run the following in steps

adjust the config.py from `src/scraper` and `src/enricher` to what industry you like

```shell
make scrape
make enrich
make analyze
```

then you got a charts and summary

## Commands

Most of the command came from python uv run, then stored in [Makefile](../Makefile). You can run them using this below

```shell
make scrape    -> scraping problems and datas
make enrich    -> enriching data with more data
make analyze   -> run analysis to create chart summary
make dev       -> mcp testing
make claude    -> add plugin to claude
```

