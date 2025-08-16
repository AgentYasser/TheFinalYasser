from __future__ import annotations

from ..llm import llm


def event_identity(theme: str, audience: str, location: str, date: str) -> str:
    system = "You are e& UAE B2B event creative lead."
    prompt = f"""
Create an event identity brief.
Theme: {theme}
Audience: {audience}
Location: {location}
Date: {date}
Deliver: key visual concept, color palette, typography, imagery style, usage examples (stage, booth, social), and a mini brand guide.
"""
    return llm.generate(system, prompt, max_tokens=1400)


def registration_ux(event_name: str) -> str:
    system = "You are e& UAE B2B event ops and UX lead."
    prompt = f"""
Design a registration landing page and form UX for {event_name}.
Include: hero messaging, form fields, validation, confirmation emails, reminders cadence, and analytics events.
"""
    return llm.generate(system, prompt, max_tokens=1200)


def agenda_and_program(event_name: str, tracks: str) -> str:
    system = "You are e& UAE B2B program director."
    prompt = f"""
Create an agenda and program design for {event_name}.
Tracks: {tracks}
Deliver: schedule blocks, session titles, speaker archetypes, stage layout notes, and motion graphics package checklist.
"""
    return llm.generate(system, prompt, max_tokens=1600)


def post_event_recap(event_name: str, target_accounts: str) -> str:
    system = "You are e& UAE B2B event marketing lead."
    prompt = f"""
Prepare a post-event recap kit for {event_name} aimed at {target_accounts}.
Include: thank-you email, survey questions, social carousel outline, highlight reel storyboard, and a 1-page ROI recap template.
"""
    return llm.generate(system, prompt, max_tokens=1600)