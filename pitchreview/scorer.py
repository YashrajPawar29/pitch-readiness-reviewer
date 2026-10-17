"""Offline scoring of a pitch against the rubric (no API key needed)."""
import re
from dataclasses import dataclass
from typing import Dict, List

from .rubric import RUBRIC, Criterion

# Claims that sound like evidence but usually aren't.
RED_FLAGS = [
    (r"\b(everyone|everybody|all students|no one else)\b", "Sweeping claim",
     "Judges distrust 'everyone'. Name the specific first customer segment."),
    (r"\bno competit(ion|ors)\b", "'No competition'",
     "There is always an alternative, even doing nothing. Show you know it."),
    (r"\b(people|users|students) (would|will) (love|use|pay)\b", "Predicted demand",
     "This is a prediction. Replace it with something customers actually did."),
    (r"\b(ai[- ]powered|revolutionary|disrupt\w*|game[- ]chang\w*)\b", "Buzzword",
     "Describe what the product does for the customer instead of the label."),
    (r"\bif (we|just) (get|capture) (1|one) ?%", "1% of a big market",
     "Top-down '1% of the market' maths is a classic red flag. Size it bottom-up."),
    (r"\b(chatgpt|claude|the ai) (said|told us|confirmed)\b", "AI as evidence",
     "AI output is a hypothesis, not customer evidence. Verify it with real people."),
]


@dataclass
class CriterionScore:
    criterion: Criterion
    score: int                # 1-5
    matched: List[str]

    @property
    def weighted(self) -> float:
        return self.score / 5 * self.criterion.weight


@dataclass
class PitchReport:
    scores: List[CriterionScore]
    red_flags: List[Dict[str, str]]
    word_count: int

    @property
    def total(self) -> int:
        return round(sum(s.weighted for s in self.scores))

    @property
    def verdict(self) -> str:
        t = self.total
        if t >= 75:
            return "Ready for judges - polish the delivery."
        if t >= 55:
            return "Promising - fill the gaps below before the Flagship Event."
        if t >= 35:
            return "Early - the story is there but evidence is thin."
        return "Not yet - go back to customer discovery."

    def weakest(self, n: int = 3) -> List[CriterionScore]:
        return sorted(self.scores, key=lambda s: (s.score, -s.criterion.weight))[:n]


def _score(criterion: Criterion, text: str) -> CriterionScore:
    matched = []
    for pattern in criterion.signals:
        m = re.search(pattern, text, re.I)
        if m:
            matched.append(m.group(0))
    # 0 hits -> 1, then +1 per distinct signal, capped at 5
    return CriterionScore(criterion, min(5, 1 + len(matched)), matched)


def review(text: str) -> PitchReport:
    scores = [_score(c, text) for c in RUBRIC]
    flags = []
    for pattern, label, advice in RED_FLAGS:
        m = re.search(pattern, text, re.I)
        if m:
            flags.append({"flag": label, "found": m.group(0), "advice": advice})
    return PitchReport(scores, flags, len(text.split()))
