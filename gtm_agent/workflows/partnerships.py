from __future__ import annotations

from ..llm import llm


def partner_program_overview(industry_focus: str, tiers: str = "Registered, Silver, Gold, Platinum") -> str:
    system = "You are e& UAE B2B partnerships lead."
    prompt = f"""
Build a one-page partner program overview for e& focused on {industry_focus}.
Include: value proposition to partners, tiering ({tiers}), benefits by tier, enablement, requirements, and how to apply.
"""
    return llm.generate(system, prompt, max_tokens=1400)


def partner_pitch_deck(product: str, target_partner: str, value_exchange: str) -> str:
    system = "You are e& UAE B2B partnerships lead."
    prompt = f"""
Create a concise 10-12 slide partner pitch deck outline for {target_partner} around {product}.
Include: market context (UAE), joint value proposition, value exchange ({value_exchange}), GTM motions, incentives, next steps.
"""
    return llm.generate(system, prompt, max_tokens=1600)


def co_sell_playbook(solution: str, partner: str, target_accounts: str) -> str:
    system = "You are e& UAE B2B co-sell lead."
    prompt = f"""
Create a co-sell playbook for {solution} with {partner} aimed at {target_accounts}.
Include: ICP, contact strategy, discovery questions, qualification, demo storyline, objection handling, ROI calculator outline, and deal progression checklist.
"""
    return llm.generate(system, prompt, max_tokens=1800)


def mdf_campaign_brief(partner: str, objective: str, budget: str) -> str:
    system = "You are e& UAE B2B partner marketing manager."
    prompt = f"""
Draft an MDF campaign brief with {partner}. Objective: {objective}. Budget: {budget}.
Include: KPIs, channels, timeline, assets list, lead management, and reporting.
"""
    return llm.generate(system, prompt, max_tokens=1400)