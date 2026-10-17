from pathlib import Path

from pitchreview.rubric import RUBRIC
from pitchreview.scorer import review

SAMPLES = Path(__file__).parent.parent / "sample_pitches"


def test_rubric_weights_sum_to_100():
    assert sum(c.weight for c in RUBRIC) == 100


def test_strong_pitch_beats_weak_pitch():
    strong = review((SAMPLES / "strong_campusgigs.md").read_text())
    weak = review((SAMPLES / "weak_studybuddy.md").read_text())
    assert strong.total > weak.total + 30
    assert len(weak.red_flags) > len(strong.red_flags)


def test_red_flags_detected():
    flags = {f["flag"] for f in review(
        "There is no competition. Everyone needs this. ChatGPT told us it's big.").red_flags}
    assert {"'No competition'", "Sweeping claim", "AI as evidence"} <= flags


def test_empty_pitch_scores_minimum():
    r = review("")
    assert all(s.score == 1 for s in r.scores)
    assert r.total == 20
