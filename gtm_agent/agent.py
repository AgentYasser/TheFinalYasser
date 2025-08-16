from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import List, Dict, Optional
from .config import settings
from .search import WebSearch
from .scraper import scrape
from .memory import store
from .llm import llm


class GTMAgent:
    def __init__(self) -> None:
        self.searcher = WebSearch()
        self.output_dir = settings.data_dir / "outputs"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def research(self, query: str, max_pages: int = 6) -> Dict:
        results = self.searcher.search(query, max_results=max_pages)
        scraped: list[dict] = []
        for r in results:
            data = scrape(r["url"])
            if not data:
                continue
            scraped.append(data)
            store.add_document(
                url=data.get("url"),
                title=data.get("title"),
                text=data.get("text", ""),
                source="web",
                tags=query,
            )
        # Summarize
        sources_md = "\n".join([f"- {d.get('title') or d.get('url')}" for d in scraped])
        joined = "\n\n".join([d.get("text", "") for d in scraped])[:24000]
        system = (
            "You are the Go-To-Market Director for e& (etisalat) UAE B2B. Synthesize research with UAE market context and B2B buyer needs."
        )
        prompt = (
            f"Query: {query}\n\nSources:\n{sources_md}\n\nContent:\n{joined}\n\nProvide: key insights, trends, competitor notes, opportunities for e& enterprise, and immediate next actions. Be concise."
        )
        summary = llm.generate(system, prompt)
        ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        out_path = self.output_dir / f"research_{ts}.md"
        out_path.write_text(summary)
        return {"summary_path": str(out_path), "sources": results}

    def generate(self, kind: str, context: Dict) -> Path:
        # Generic interface to workflows via CLI. The CLI modules will handle specifics.
        ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        path = self.output_dir / f"{kind}_{ts}.md"
        system = (
            "You are the GTM Director for e& UAE B2B. Produce practical, on-brand content ready for client-facing use. Include bullets, headlines, and clear CTAs."
        )
        prompt = f"Task: {kind}\n\nContext:\n{context}\n\nDeliver a complete, polished artifact in Markdown."
        text = llm.generate(system, prompt, max_tokens=2400)
        path.write_text(text)
        return path


def get_agent() -> GTMAgent:
    return GTMAgent()