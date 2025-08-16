from __future__ import annotations

from typing import List, Dict, Optional
from openai import OpenAI
from .config import settings


class LLM:
    def __init__(self) -> None:
        self.enabled = bool(settings.openai_api_key)
        self.client = OpenAI(api_key=settings.openai_api_key) if self.enabled else None
        self.model = settings.model

    def generate(self, system: str, prompt: str, *, temperature: float = 0.3, max_tokens: int = 1200) -> str:
        if self.enabled and self.client:
            resp = self.client.chat.completions.create(
                model=self.model,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            )
            return resp.choices[0].message.content or ""
        # Fallback outline if no API key
        return f"SYSTEM: {system}\n\nPROMPT: {prompt}\n\n[LLM disabled. Provide a concise, bulletized outline covering: objective, audience, key messages, channels, KPIs, timeline, and next actions.]"


llm = LLM()