"""Claude as a mock angel-investor judge.

Only used when an ANTHROPIC_API_KEY is available.
"""
import json
import os
from typing import Dict

from .rubric import RUBRIC

MODEL = "claude-opus-5-5"


def _system_prompt() -> str:
    lines = "\n".join(f"- {c.name} (weight {c.weight}): {c.looks_for}" for c in RUBRIC)
    return f"""You are an experienced angel investor judging an early-stage student venture
pitch. Score it against this rubric, 1-5 per criterion:

{lines}

Rules:
- Quote the pitch to justify each score. If something is missing, say it is missing.
- Customer evidence means what real customers did. AI-generated research, opinions and
  predicted demand are not evidence.
- Give feedback as a coach: questions and specific next steps, not a rewritten pitch.
- Be candid but kind. These are students learning to build ventures."""


SCHEMA = {
    "type": "object",
    "properties": {
        "scores": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "criterion": {"type": "string", "enum": [c.name for c in RUBRIC]},
                    "score": {"type": "integer", "enum": [1, 2, 3, 4, 5]},
                    "quote": {"type": "string"},
                    "feedback": {"type": "string"},
                },
                "required": ["criterion", "score", "quote", "feedback"],
                "additionalProperties": False,
            },
        },
        "strongest_point": {"type": "string"},
        "biggest_risk": {"type": "string"},
        "judge_questions": {"type": "array", "items": {"type": "string"}},
        "next_steps": {"type": "array", "items": {"type": "string"}},
        "would_take_a_second_meeting": {"type": "boolean"},
    },
    "required": ["scores", "strongest_point", "biggest_risk", "judge_questions",
                 "next_steps", "would_take_a_second_meeting"],
    "additionalProperties": False,
}


def is_available() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def judge(pitch: str) -> Dict:
    import anthropic  # lazy import: offline mode doesn't need the SDK

    client = anthropic.Anthropic()
    response = client.beta.messages.create(
        model=MODEL,
        max_tokens=16000,
        system=_system_prompt(),
        messages=[{"role": "user", "content": f"<pitch>\n{pitch}\n</pitch>"}],
        betas=["server-side-fallback-2026-07-01"],
        extra_body={
            "output_config": {"effort": "medium",
                              "format": {"type": "json_schema", "schema": SCHEMA}},
            "fallbacks": "default",
        },
    )
    if response.stop_reason == "refusal":
        raise RuntimeError("Claude declined to review this pitch.")
    if response.stop_reason == "max_tokens":
        raise RuntimeError("The review was cut off. Try a shorter pitch.")
    text = next(b.text for b in response.content if b.type == "text")
    return json.loads(text)
