from __future__ import annotations

from typing import Dict
from ..llm import llm


def messaging_house(company: str, product: str, audience: str, tone: str = "authoritative, solutions-driven") -> str:
    system = "You are e& UAE B2B GTM Director. Create crisp, enterprise-grade messaging."
    prompt = f"""
Company: {company}
Product: {product}
Audience: {audience}
Tone: {tone}

Deliver a messaging house with:
- Value proposition (1-2 lines)
- 5-7 proof points (data-backed if possible)
- 6-8 benefit bullets mapped to pains
- 3 tagline options
- Elevator pitch (60-90 words)
- Objection handling bullets
"""
    return llm.generate(system, prompt, max_tokens=1800)


def positioning_deck_outline(company: str, product: str, competitors: str, audience: str) -> str:
    system = "You are e& UAE B2B GTM Director. Create a sharp positioning and narrative deck outline."
    prompt = f"""
Company: {company}
Product: {product}
Competitors: {competitors}
Audience: {audience}

Provide a 12-16 slide outline with slide titles, 2-4 bullets each, and a call-to-action.
"""
    return llm.generate(system, prompt, max_tokens=1600)


def website_brief(company: str, product: str, audience: str, pages: str = "Home, Solutions, Industries, Resources, Contact") -> str:
    system = "You are e& UAE B2B GTM Director and UX lead."
    prompt = f"""
Craft a website/landing page brief for {company} - {product} for {audience}.
Include:
- IA and sitemap
- Wireframe notes for hero, social proof, value stack, features grid, pricing/CTA
- Visual direction (color, typography, imagery)
- SEO targets (primary/secondary keywords, meta examples)
- Sample copy blocks (hero H1/H2, CTA, 3 features)
- Tracking plan (KPIs, events)
"""
    return llm.generate(system, prompt, max_tokens=2000)


def performance_ads_briefs(company: str, product: str, audiences: str, channels: str = "LinkedIn, Google, Programmatic") -> str:
    system = "You are e& UAE B2B performance marketing lead."
    prompt = f"""
Create performance ad briefs for {company} {product} targeting {audiences} across {channels}.
Deliver:
- 5x static concepts (headlines, body, CTA, visual notes)
- 3x HTML5/motion concepts (6s/10s/15s scripts)
- 5x keywords themes and negatives for search
- UTM schema and test plan
"""
    return llm.generate(system, prompt, max_tokens=1600)