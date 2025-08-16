from __future__ import annotations

import json
from pathlib import Path
import typer
from rich import print
from .agent import get_agent
from .search import search as web_search
from .scraper import scrape, crawl
from .memory import store
from .workflows import marketing, partnerships, events

app = typer.Typer(help="e& UAE B2B GTM Director Agent")


@app.command()
def search(query: str, max_results: int = 10):
    """Search the web across providers and print results."""
    results = web_search(query, max_results=max_results)
    print(results)


@app.command()
def save(url: str):
    """Scrape a URL and save to memory."""
    data = scrape(url)
    if not data:
        raise typer.Exit(code=1)
    store.add_document(url=url, title=data.get("title"), text=data.get("text", ""), source="web")
    print({"saved": True, "title": data.get("title")})


@app.command()
def mem(query: str, limit: int = 10):
    """Search persistent memory (FTS)."""
    print(store.search(query, limit=limit))


@app.command()
def crawl_site(url: str, max_pages: int = 10, same_domain_only: bool = True):
    data = crawl(url, max_pages=max_pages, same_domain_only=same_domain_only)
    for d in data:
        store.add_document(url=d.get("url"), title=d.get("title"), text=d.get("text", ""), source="web")
    print({"crawled": len(data)})


@app.command()
def research(query: str, max_pages: int = 6):
    agent = get_agent()
    out = agent.research(query, max_pages=max_pages)
    print(out)


@app.command("marketing-messaging")
def marketing_messaging(company: str, product: str, audience: str, tone: str = "authoritative, solutions-driven"):
    text = marketing.messaging_house(company, product, audience, tone)
    Path("output_marketing_messaging.md").write_text(text)
    print("Wrote output_marketing_messaging.md")


@app.command("marketing-positioning")
def marketing_positioning(company: str, product: str, competitors: str, audience: str):
    text = marketing.positioning_deck_outline(company, product, competitors, audience)
    Path("output_marketing_positioning.md").write_text(text)
    print("Wrote output_marketing_positioning.md")


@app.command("marketing-website")
def marketing_website(company: str, product: str, audience: str):
    text = marketing.website_brief(company, product, audience)
    Path("output_marketing_website.md").write_text(text)
    print("Wrote output_marketing_website.md")


@app.command("marketing-ads")
def marketing_ads(company: str, product: str, audiences: str, channels: str = "LinkedIn, Google, Programmatic"):
    text = marketing.performance_ads_briefs(company, product, audiences, channels)
    Path("output_marketing_ads.md").write_text(text)
    print("Wrote output_marketing_ads.md")


@app.command("partner-overview")
def partner_overview(industry_focus: str):
    text = partnerships.partner_program_overview(industry_focus)
    Path("output_partner_overview.md").write_text(text)
    print("Wrote output_partner_overview.md")


@app.command("partner-pitch")
def partner_pitch(product: str, target_partner: str, value_exchange: str):
    text = partnerships.partner_pitch_deck(product, target_partner, value_exchange)
    Path("output_partner_pitch.md").write_text(text)
    print("Wrote output_partner_pitch.md")


@app.command("co-sell")
def co_sell(solution: str, partner: str, target_accounts: str):
    text = partnerships.co_sell_playbook(solution, partner, target_accounts)
    Path("output_co_sell.md").write_text(text)
    print("Wrote output_co_sell.md")


@app.command("mdf-brief")
def mdf_brief(partner: str, objective: str, budget: str):
    text = partnerships.mdf_campaign_brief(partner, objective, budget)
    Path("output_mdf_brief.md").write_text(text)
    print("Wrote output_mdf_brief.md")


@app.command("event-identity")
def event_identity(theme: str, audience: str, location: str, date: str):
    text = events.event_identity(theme, audience, location, date)
    Path("output_event_identity.md").write_text(text)
    print("Wrote output_event_identity.md")


@app.command("event-registration")
def event_registration(event_name: str):
    text = events.registration_ux(event_name)
    Path("output_event_registration.md").write_text(text)
    print("Wrote output_event_registration.md")


@app.command("event-agenda")
def event_agenda(event_name: str, tracks: str):
    text = events.agenda_and_program(event_name, tracks)
    Path("output_event_agenda.md").write_text(text)
    print("Wrote output_event_agenda.md")


@app.command("event-recap")
def event_recap(event_name: str, target_accounts: str):
    text = events.post_event_recap(event_name, target_accounts)
    Path("output_event_recap.md").write_text(text)
    print("Wrote output_event_recap.md")


def run():
    app()


if __name__ == "__main__":
    run()