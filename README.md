# 🎤 Pitch Readiness Reviewer

**Score a startup pitch the way an angel investor would.** Paste a pitch script or one-pager. You get a 0–100 readiness score against an 8-part investor rubric, the red-flag phrases judges notice, and the coaching questions to close the gaps before demo day. Turn on Claude to get a mock judge's full verdict.

## The rubric

| Criterion | Weight | What judges look for |
|---|---|---|
| Problem | 15 | A specific, painful problem for a clearly named customer |
| Customer evidence | 20 | Primary research: interviews, observed behaviour, numbers |
| Solution & MVP | 15 | A focused MVP that tests the riskiest assumption |
| Market | 10 | A credible, bottom-up market size |
| Business model | 15 | Who pays, how much, and why the unit economics work |
| Traction | 10 | Sign-ups, pilots, letters of intent, retention |
| Competition & advantage | 5 | Honest alternatives (including doing nothing) and why you win |
| Team & ask | 10 | Why this team, and a clear amount, use of funds, and milestones |

The rubric is defined in [`pitchreview/rubric.py`](pitchreview/rubric.py). Edit it to match any program's judging criteria.

## What it does

- **Readiness score and verdict.** Weighted score from 0 to 100, plus a plain-English verdict ("Promising: fill the gaps below…").
- **Biggest gaps.** Your three weakest criteria, each with the questions a coach would ask. It doesn't write the answers for you.
- **Red-flag detector.** Catches phrases that hurt credibility with investors: "no competition", "everyone needs this", "if we capture 1% of the market", buzzwords, predicted demand, and treating ChatGPT's answers as evidence.
- **Claude as judge** (optional). Claude (`claude-opus-5-5`) scores each criterion with a quote from your pitch, names the strongest point and biggest risk, lists the questions judges will likely ask, and says whether it would take a second meeting. Results come back as schema-validated JSON.

The offline rubric scorer runs **with no API key**. Two **fictional** sample pitches, one strong and one weak, are in [`sample_pitches/`](sample_pitches) so you can compare them (the strong one scores 83, the weak one 32).

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

To turn on Claude as judge:

```bash
export ANTHROPIC_API_KEY=your-key-here
streamlit run app.py
```

Run the tests:

```bash
python -m pytest
```

## Project structure

```
app.py                  Streamlit UI
pitchreview/rubric.py   The investor rubric: weights, signals, coaching questions
pitchreview/scorer.py   Offline scoring and red-flag detection
pitchreview/ai.py       Claude mock-judge with structured JSON output
sample_pitches/         Fictional strong and weak example pitches
tests/                  pytest unit tests
```

## Design choices

- **Coach, don't author.** Feedback comes as questions and next steps, not a rewritten pitch. The team keeps ownership of the venture.
- **Evidence over enthusiasm.** The highest-weighted criterion is customer evidence. The prompt tells Claude that AI-generated research and predicted demand don't count.
- **Transparent scoring.** The offline score shows which phrases triggered each criterion, so the score is never a black box.

## License

MIT
