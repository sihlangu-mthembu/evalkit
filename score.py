"""Scoring logic for evalkit.

Compares one model response with a question's golden answer and returns a
label, a score and a list of flags. Pure Python, no dependencies.

Labels, checked in this order:
    correct    the golden answer (or an accepted alias) appears in the response
    no_answer  the model declined or said it could not find the answer
    distractor the model gave a known wrong answer listed for the question
    partial    a date question where only the correct year appears
    wrong      anything else
"""

import re
import unicodedata

LABEL_POINTS = {"correct": 1.0, "partial": 0.5, "no_answer": 0.0, "distractor": 0.0, "wrong": 0.0}

MONTHS = {
    name: number
    for number, name in enumerate(
        ["january", "february", "march", "april", "may", "june", "july",
         "august", "september", "october", "november", "december"],
        start=1,
    )
}
_MONTH_RE = "|".join(MONTHS)

ABSTAIN_PATTERNS = [
    r"\bnot specified\b",
    r"\bcouldn'?t\b",
    r"\bcould not\b",
    r"\bunable to\b",
    r"\bno (?:reliable )?information\b",
    r"\bnot (?:publicly )?available\b",
    r"\bi don'?t know\b",
    r"\bnone of the sources\b",
    r"\bcannot (?:find|determine|confirm)\b",
]


def normalise(text):
    """Lower-case, fold accents, turn '&' into 'and' and strip punctuation."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = text.lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_dates(text):
    """Return a set of (year, month, day) tuples found in the text.

    Handles '2 June 1943', 'June 2, 1943', '2nd June 1943' and '1943-06-02'.
    """
    lowered = text.lower()
    found = set()
    for day, month, year in re.findall(
        rf"\b(\d{{1,2}})(?:st|nd|rd|th)?\s+({_MONTH_RE})\s*,?\s+(\d{{4}})\b", lowered
    ):
        found.add((int(year), MONTHS[month], int(day)))
    for month, day, year in re.findall(
        rf"\b({_MONTH_RE})\s+(\d{{1,2}})(?:st|nd|rd|th)?,?\s+(\d{{4}})\b", lowered
    ):
        found.add((int(year), MONTHS[month], int(day)))
    for year, month, day in re.findall(r"\b(\d{4})-(\d{2})-(\d{2})\b", lowered):
        found.add((int(year), int(month), int(day)))
    return found


def extract_numbers(text):
    """Return every number in the text as a float ('3,300' -> 3300.0)."""
    numbers = set()
    for raw in re.findall(r"(?<![\w.])\d[\d,]*(?:\.\d+)?", text):
        cleaned = raw.rstrip(",").replace(",", "")
        try:
            numbers.add(float(cleaned))
        except ValueError:
            continue
    return numbers


def _parse_golden_date(value):
    dates = extract_dates(value)
    return next(iter(dates)) if dates else None


def matches(response, target):
    """True if `target` (a date, number or phrase) appears in `response`."""
    target_date = _parse_golden_date(target)
    if target_date:
        return target_date in extract_dates(response)
    plain = target.replace(",", "").replace("£", "").replace("$", "").strip()
    if re.fullmatch(r"\d+(?:\.\d+)?", plain):
        return float(plain) in extract_numbers(response)
    return normalise(target) in normalise(response)


def abstained(response):
    lowered = response.lower()
    return any(re.search(pattern, lowered) for pattern in ABSTAIN_PATTERNS)


def score_response(question, response):
    """Score one response. Returns {'label', 'points', 'flags'}."""
    golden = [question["answer"], *question.get("accept", [])]
    distractors = question.get("distractors", [])

    flags = []
    hit_distractors = [d for d in distractors if matches(response, d)]
    if hit_distractors:
        flags.append("mentions_distractor:" + "|".join(hit_distractors))
    if abstained(response):
        flags.append("abstained")

    if any(matches(response, g) for g in golden):
        label = "correct"
    elif "abstained" in flags:
        label = "no_answer"
    elif hit_distractors:
        label = "distractor"
    elif question.get("answer_type") == "date" and _year_only(question["answer"], response):
        label = "partial"
    else:
        label = "wrong"
    return {"label": label, "points": LABEL_POINTS[label], "flags": flags}


def _year_only(golden_answer, response):
    golden_date = _parse_golden_date(golden_answer)
    return bool(golden_date) and float(golden_date[0]) in extract_numbers(response)
