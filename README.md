# evalkit

A small Python harness for evaluating how well large language models answer **hard, source-verified research questions**, and for explaining *how* they fail when they get them wrong.

I built it while writing open-web research tasks designed to trip up frontier AI models. Each question has a single defensible answer, backed by exact quotes from at least one public source, plus a list of known "distractors": plausible wrong answers a model is likely to give.

## What it does

1. Loads a question set (`data/questions.jsonl`) with golden answers, sources, quotes and distractors.
2. Loads model responses from a file, or asks a model live through the Anthropic API.
3. Scores every response and labels it:

| Label | Meaning | Points |
| --- | --- | --- |
| `correct` | The golden answer (or an accepted alias) appears | 1 |
| `partial` | Date questions only: the right year but not the full date | 0.5 |
| `distractor` | The model gave one of the known wrong answers | 0 |
| `no_answer` | The model declined or said it couldn't find the answer | 0 |
| `wrong` | Anything else | 0 |

4. Writes a Markdown report (`reports/report.md`) with a per-model summary, a comparison of the automatic labels against my hand labels, and a breakdown of every failure with the evidence that proves the golden answer.

## Quick start

Needs Python 3.10 or newer. No packages to install; it uses only the standard library.

```bash
python run.py                      # score the bundled responses (free, offline)
python -m unittest discover tests  # run the tests
```

Then open `reports/report.md`.

## What's in the data

- **12 questions** about Johannesburg architectural, medical and civic history, most needing two hops across sources that don't reference each other.
- **`responses/observed_2026-10.jsonl`:** 5 real answers I collected by hand on 25 October 2026 from Claude Opus 5 (claude.ai, web search on), the Gemini app (Flash-Lite) and Google Search's AI Overview, each with my own label and note.
- **`responses/demo_synthetic.jsonl`:** 12 **made-up** answers written to exercise every scoring label. They are not output from any real model.

### Sample result (real responses)

| Model | Responses | Correct | Failure |
| --- | --- | --- | --- |
| Claude Opus 5 (web search) | 3 | 2 | Could not find the 1967 bed count (honest `no_answer`) |
| Gemini app (Flash-Lite) | 1 | 0 | Gave the business partner's death year (1967) instead of the Halifax architect's (`distractor`) |
| Google Search AI Overview | 1 | 0 | Said the bed count was not in public records and offered today's figure (`no_answer`) |

The automatic scorer matched my hand labels on 5 of 5 responses. That is a small sample, not a benchmark result.

## Running against a live model (optional)

```bash
# Windows Command Prompt
set ANTHROPIC_API_KEY=your-key-here
python run.py --live --model claude-sonnet-5-5
```

This costs a few cents. Answers are saved to `responses/live_<model>_<date>.jsonl` and scored. Live mode sends the question **without web search**, so it tests what the model knows rather than how well it browses.

**Never commit your API key.** `.gitignore` excludes `.env` files.

## Adding your own questions

Add one JSON object per line to `data/questions.jsonl`:

```json
{"id": "q13", "hops": 2, "answer_type": "date", "answer": "2 June 1943", "accept": [],
 "question": "...", "distractors": ["1967"],
 "sources": [{"title": "...", "url": "https://...", "quote": "exact sentence from the source"}],
 "notes": "why the distractor is tempting"}
```

`answer_type` is `date`, `number` or `text`. Good questions have one defensible answer, don't change over time, and need at least two sources.

## Limitations

- Matching is rule-based. A response that mentions the golden answer only in passing (for example, "it was not 80") would still score as correct.
- The scorer can't tell an honest "I couldn't find it" from a false claim that the information doesn't exist. Both are labelled `no_answer`, and the human note captures the difference.
- Observed responses were copied by hand from chat interfaces, and some long answers are trimmed (marked `[...]`).
- 12 questions and 5 real responses is a demonstration, not a benchmark.

## Project structure

```
evalkit/
├── run.py               # loads data, runs scoring, writes the report
├── score.py             # scoring rules (dates, numbers, text, abstentions, distractors)
├── data/questions.jsonl
├── responses/           # observed and synthetic responses
├── reports/             # generated report.md and results.csv
└── tests/test_score.py
```

## Author

Sihlangu Mthembu, AI evaluation and data analysis. Economics & Politics, University of Cape Town.
