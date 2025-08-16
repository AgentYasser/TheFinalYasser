from __future__ import annotations

import os
import json
from typing import List, Dict
import httpx
from duckduckgo_search import DDGS
from .config import settings


class WebSearch:
    def __init__(self) -> None:
        self.headers = {"User-Agent": settings.user_agent}

    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        results: list[dict] = []
        results.extend(self._ddg(query, max_results=max_results))
        if settings.brave_search_api_key:
            results.extend(self._brave(query, max_results=max_results))
        if settings.bing_search_api_key:
            results.extend(self._bing(query, max_results=max_results))
        if settings.serpapi_api_key:
            results.extend(self._serpapi(query, max_results=max_results))
        if settings.tavily_api_key:
            results.extend(self._tavily(query, max_results=max_results))
        # Deduplicate by URL while preserving order
        seen = set()
        deduped: list[dict] = []
        for r in results:
            url = r.get("url") or r.get("link")
            if not url:
                continue
            if url in seen:
                continue
            seen.add(url)
            deduped.append(
                {
                    "title": r.get("title") or r.get("name") or r.get("header"),
                    "url": url,
                    "snippet": r.get("snippet") or r.get("description") or r.get("body"),
                    "source": r.get("source") or r.get("engine") or r.get("provider"),
                }
            )
        return deduped[:max_results]

    def _ddg(self, query: str, max_results: int = 10) -> List[Dict]:
        out: list[dict] = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, region="ae-en", safesearch="moderate", max_results=max_results):
                out.append(
                    {
                        "title": r.get("title"),
                        "url": r.get("href"),
                        "snippet": r.get("body"),
                        "source": "duckduckgo",
                    }
                )
        return out

    def _brave(self, query: str, max_results: int = 10) -> List[Dict]:
        try:
            url = "https://api.search.brave.com/res/v1/web/search"
            params = {"q": query, "count": max_results}
            headers = {**self.headers, "X-Subscription-Token": settings.brave_search_api_key}
            resp = httpx.get(url, params=params, headers=headers, timeout=20)
            resp.raise_for_status()
            data = resp.json()
            web = data.get("web", {}).get("results", [])
            return [
                {
                    "title": r.get("title"),
                    "url": r.get("url"),
                    "snippet": r.get("description"),
                    "source": "brave",
                }
                for r in web
            ]
        except Exception:
            return []

    def _bing(self, query: str, max_results: int = 10) -> List[Dict]:
        try:
            url = "https://api.bing.microsoft.com/v7.0/search"
            params = {"q": query, "count": max_results, "mkt": "en-AE"}
            headers = {**self.headers, "Ocp-Apim-Subscription-Key": settings.bing_search_api_key}
            resp = httpx.get(url, params=params, headers=headers, timeout=20)
            resp.raise_for_status()
            data = resp.json()
            web = data.get("webPages", {}).get("value", [])
            return [
                {
                    "title": r.get("name"),
                    "url": r.get("url"),
                    "snippet": r.get("snippet"),
                    "source": "bing",
                }
                for r in web
            ]
        except Exception:
            return []

    def _serpapi(self, query: str, max_results: int = 10) -> List[Dict]:
        try:
            url = "https://serpapi.com/search.json"
            params = {
                "engine": "google",
                "q": query,
                "num": max_results,
                "location": "United Arab Emirates",
                "api_key": settings.serpapi_api_key,
            }
            resp = httpx.get(url, params=params, headers=self.headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            web = data.get("organic_results", [])
            return [
                {
                    "title": r.get("title"),
                    "url": r.get("link"),
                    "snippet": r.get("snippet"),
                    "source": "serpapi",
                }
                for r in web
            ]
        except Exception:
            return []

    def _tavily(self, query: str, max_results: int = 10) -> List[Dict]:
        try:
            url = "https://api.tavily.com/search"
            payload = {
                "api_key": settings.tavily_api_key,
                "query": query,
                "max_results": max_results,
                "search_depth": "basic",
            }
            resp = httpx.post(url, json=payload, headers=self.headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            web = data.get("results", [])
            return [
                {
                    "title": r.get("title"),
                    "url": r.get("url"),
                    "snippet": r.get("content"),
                    "source": "tavily",
                }
                for r in web
            ]
        except Exception:
            return []


def search(query: str, max_results: int = 10) -> List[Dict]:
    return WebSearch().search(query, max_results=max_results)