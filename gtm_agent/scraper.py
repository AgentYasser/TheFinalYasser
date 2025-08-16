from __future__ import annotations

import re
import time
import urllib.parse
from typing import Dict, List, Optional, Tuple, Set
import httpx
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from .config import settings


_robot_cache: dict[str, RobotFileParser] = {}
_last_request_ts: float = 0.0
_MIN_DELAY_S = 0.8


def _rate_limit() -> None:
    global _last_request_ts
    now = time.time()
    if now - _last_request_ts < _MIN_DELAY_S:
        time.sleep(_MIN_DELAY_S - (now - _last_request_ts))
    _last_request_ts = time.time()


def allowed_by_robots(url: str, user_agent: str | None = None) -> bool:
    try:
        parsed = urllib.parse.urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        if robots_url not in _robot_cache:
            rp = RobotFileParser()
            _rate_limit()
            resp = httpx.get(robots_url, headers={"User-Agent": user_agent or settings.user_agent}, timeout=10)
            if resp.status_code >= 400:
                _robot_cache[robots_url] = None  # type: ignore
                return True
            rp.parse(resp.text.splitlines())
            _robot_cache[robots_url] = rp
        rp = _robot_cache[robots_url]
        if rp is None:
            return True
        return rp.can_fetch(user_agent or settings.user_agent, url)
    except Exception:
        return True


def fetch(url: str, timeout: int = 30) -> Optional[str]:
    if not allowed_by_robots(url):
        return None
    headers = {"User-Agent": settings.user_agent}
    _rate_limit()
    resp = httpx.get(url, headers=headers, timeout=timeout, follow_redirects=True)
    if resp.status_code >= 400:
        return None
    return resp.text


def extract_readable(html: str) -> Tuple[str, str, List[str]]:
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "noscript", "iframe", "svg"]):
        tag.decompose()
    title = (soup.title.string or "").strip() if soup.title else ""

    main = soup.find("main") or soup.find("article") or soup.find("section") or soup.body
    paragraphs = []
    headings = []
    if main:
        for h in main.find_all(["h1", "h2", "h3", "h4"]):
            text = h.get_text(" ", strip=True)
            if text:
                headings.append(text)
        for p in main.find_all(["p", "li"]):
            text = p.get_text(" ", strip=True)
            if text and len(text.split()) > 3:
                paragraphs.append(text)
    content = "\n\n".join(paragraphs)
    return title, content, headings


EAND_DOMAINS = {
    "eand.com",
    "eandenterprise.com",
    "eandenterprise.ae",
    "etisalat.ae",
}


def extract_eand_product_features(url: str, html: str) -> Dict:
    title, content, headings = extract_readable(html)
    features = []
    benefits = []

    soup = BeautifulSoup(html, "lxml")
    for sect_name in ["feature", "benefit", "advantage", "capabil", "why", "value"]:
        for node in soup.find_all(lambda tag: tag.name in ["section", "div", "ul"] and sect_name in (" ".join(tag.get("class", [])) + " " + (tag.get("id") or "")).lower()):
            for li in node.find_all("li"):
                text = li.get_text(" ", strip=True)
                if not text or len(text) < 5:
                    continue
                if "benefit" in sect_name or "why" in sect_name or "value" in sect_name:
                    benefits.append(text)
                else:
                    features.append(text)

    if not features:
        for line in content.split("\n"):
            line = line.strip()
            if 5 < len(line) < 140 and (":" in line or line.endswith(".")):
                features.append(line)

    return {
        "title": title,
        "headings": headings,
        "features": list(dict.fromkeys(features))[:30],
        "benefits": list(dict.fromkeys(benefits))[:30],
        "raw_text": content,
    }


def scrape(url: str) -> Optional[Dict]:
    html = fetch(url)
    if not html:
        return None
    title, text, headings = extract_readable(html)
    data = {"url": url, "title": title, "text": text, "headings": headings}
    host = urllib.parse.urlparse(url).netloc
    if any(host.endswith(d) for d in EAND_DOMAINS):
        data["eand_extract"] = extract_eand_product_features(url, html)
    return data


def crawl(seed_url: str, max_pages: int = 10, same_domain_only: bool = True) -> List[Dict]:
    parsed_seed = urllib.parse.urlparse(seed_url)
    domain = parsed_seed.netloc
    to_visit: list[str] = [seed_url]
    visited: Set[str] = set()
    results: list[dict] = []

    while to_visit and len(results) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)
        html = fetch(url)
        if not html:
            continue
        data = scrape(url)
        if data:
            results.append(data)
        soup = BeautifulSoup(html, "lxml")
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            next_url = urllib.parse.urljoin(url, href)
            p = urllib.parse.urlparse(next_url)
            if same_domain_only and p.netloc != domain:
                continue
            if p.scheme not in {"http", "https"}:
                continue
            if next_url in visited or next_url in to_visit:
                continue
            if any(ext in p.path.lower() for ext in [".pdf", ".jpg", ".png", ".zip", ".gif", ".svg", ".mp4", ".mov"]):
                continue
            to_visit.append(next_url)

    return results