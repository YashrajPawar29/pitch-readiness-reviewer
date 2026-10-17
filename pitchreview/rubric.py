"""An angel-investor style rubric for early-stage pitches.

Each criterion lists what a judge looks for, simple text signals that suggest
the pitch covers it, and the coaching questions to ask when it doesn't.
"""
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Criterion:
    key: str
    name: str
    weight: int               # relative importance, sums to 100
    looks_for: str
    signals: List[str]        # regexes; more distinct hits -> higher score
    questions: List[str]      # asked when the criterion scores low


RUBRIC: List[Criterion] = [
    Criterion(
        "problem", "Problem", 15,
        "A specific, painful problem for a clearly named customer.",
        [r"\bproblem\b", r"\bpain\b", r"\bstruggl\w*", r"\bfrustrat\w*", r"\bwast\w*",
         r"\bcost(s|ing)?\b", r"\bhours?\b"],
        ["Who exactly has this problem? Can you name one real person?",
         "How do they solve it today, and what does that cost them?"]),
    Criterion(
        "customer_evidence", "Customer evidence", 20,
        "Primary research: interviews, observed behaviour, numbers - not opinions.",
        [r"\binterview\w*", r"\bsurvey\w*", r"\bwe (talked|spoke) (to|with)\b",
         r"\b\d+\s*(students|users|customers|people|interviews|respondents)\b",
         r"\b\d+\s?%", r"\bquote\b|“|\""],
        ["How many customers did you talk to, and what did they *do* (not say)?",
         "Which of your assumptions did the interviews contradict?"]),
    Criterion(
        "solution", "Solution & MVP", 15,
        "A focused MVP that tests the riskiest assumption, ideally used by real people.",
        [r"\bmvp\b", r"\bprototype\b", r"\bpilot\b", r"\bbeta\b", r"\btested\b",
         r"\busability\b", r"\bdemo\b"],
        ["What is the smallest thing you built to test your riskiest assumption?",
         "What did users do with the prototype that surprised you?"]),
    Criterion(
        "market", "Market", 10,
        "A credible, bottom-up estimate of who would pay and how many of them exist.",
        [r"\bmarket\b", r"\btam\b|\bsam\b|\bsom\b", r"\$\s?\d+(\.\d+)?\s?(b|bn|billion|m|mn|million)\b",
         r"\b\d[\d,]*\s+(colleges|universities|schools|businesses|companies)\b"],
        ["Can you size the market bottom-up (number of buyers x price) instead of top-down?",
         "Which segment will you win first, and why them?"]),
    Criterion(
        "business_model", "Business model", 15,
        "Who pays, how much, and why the unit economics can work.",
        [r"\bsubscription\b", r"\bpric\w*", r"\bper (month|year|user|seat)\b",
         r"\brevenue\b", r"\bfreemium\b", r"\b(cac|ltv|margin)\b", r"\$\s?\d+\s?/\s?(mo|month|yr|year)"],
        ["Who is the paying customer - is it the same person as the user?",
         "What evidence do you have that they will pay this price?"]),
    Criterion(
        "traction", "Traction", 10,
        "Signals of real demand: sign-ups, pilots, letters of intent, retention.",
        [r"\bwaitlist\b", r"\bsign[- ]?ups?\b", r"\bpilot\b", r"\bloi\b|letter of intent",
         r"\bretention\b", r"\bweekly active\b|\bactive users\b", r"\bpaying\b"],
        ["What has anyone committed - time, money, or reputation - to your solution?",
         "What number will you move in the next 30 days?"]),
    Criterion(
        "competition", "Competition & advantage", 5,
        "Honest view of alternatives (including doing nothing) and why you win.",
        [r"\bcompetit\w*", r"\balternative\w*", r"\binstead\b", r"\bunlike\b",
         r"\bdifferent\w*", r"\badvantage\b|\bmoat\b"],
        ["What do customers use today instead, including spreadsheets or doing nothing?",
         "Why can't the biggest incumbent copy you next quarter?"]),
    Criterion(
        "team_ask", "Team & ask", 10,
        "Why this team, and a clear ask: amount, use of funds, milestones.",
        [r"\bteam\b", r"\bwe are\b|\bour team\b", r"\braising\b", r"\bask\b",
         r"\buse of funds\b", r"\bmilestone\w*", r"\$\s?\d+\s?(k|m)\b"],
        ["Why is your team the one to solve this?",
         "What exactly are you asking for, and what milestone will it get you to?"]),
]

assert sum(c.weight for c in RUBRIC) == 100
