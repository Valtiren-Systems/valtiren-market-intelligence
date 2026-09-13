.PHONY: scrape enrich 

scrape:
	uv run python -m src.scraper.main

enrich:
	uv run python -m src.enricher.main

dev:
	uv run mcp dev src/mcp_server/server.py

claude:
	uv run mcp install src/mcp_server/server.py \
		--with pandas

analyze:
	uv run src/pattern_observer/observer.py
