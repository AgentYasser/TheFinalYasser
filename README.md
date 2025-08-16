# e& B2B GTM Director Agent

An AI agent tailored as the Go-To-Market Director for e& (etisalat) in the UAE B2B division. It can research markets in real time, persist findings, generate sales/marketing/event assets, and orchestrate strategic partnership workflows.

## Features
- Web research across multiple providers (DuckDuckGo out of the box; Brave/Bing/SerpAPI/Tavily via API keys)
- Persistent memory using SQLite FTS for fast semantic-like keyword recall
- Targeted scraping and focused extraction for e& domains
- LLM-powered content generation (OpenAI). Fallback templating if no API key set
- Turnkey workflows for Marketing, Strategic Partnerships, and Events
- Simple CLI for day-to-day tasks

## Quickstart
1. Python 3.10+
2. Install deps:
```bash
pip install -r requirements.txt
```
3. Copy environment template and edit:
```bash
cp .env.example .env
```
4. Try a research run (no API key required):
```bash
python -m gtm_agent search "UAE SMB cloud adoption 2025"
```
5. Generate a messaging house (requires OPENAI_API_KEY):
```bash
python -m gtm_agent marketing messaging-house \
  --company "e& enterprise" \
  --product "Managed SD-WAN" \
  --audience "CIOs at UAE mid-market enterprises" \
  --tone "authoritative, solutions-driven"
```

## Environment variables
See `.env.example` for optional providers and configuration.

## Data & Persistence
By default, data lives in `~/.gtm_agent`. Override with `GTM_AGENT_DATA_DIR`.

## Legal & Ethics
- Always review robots.txt before crawling. This tool respects robots.txt by default and rate-limits requests.
- Ensure you have rights to use and distribute any scraped content.

## License
For internal enablement. Add your license here.