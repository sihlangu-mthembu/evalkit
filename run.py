"""evalkit: score LLM answers to hard, source-verified research questions.

Usage:
    python run.py                         # score the bundled responses (free, offline)
    python run.py --responses FILE.jsonl  # score your own responses file
    python run.py --live --model MODEL    # ask a model via the Anthropic API, then score

Writes reports/report.md and reports/results.csv.
"""

import argparse
import csv
import datetime
import json
import os
import pathlib
import sys
import urllib.request
from typing import Any

from score import score_response

ROOT = pathlib.Path(__file__).resolve().parent
DEFAULT_RESPONSES = [ROOT / "responses" / "observed_2026-10.jsonl", ROOT / "responses" / "demo_synthetic.jsonl"]
LABELS = ["correct", "partial", "distractor", "no_answer", "wrong"]


def load_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def ask_anthropic(question: str, model: str) -> str:
    """Send one question to the Anthropic Messages API using only the standard library."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("Set ANTHROPIC_API_KEY first (see README). Never commit your key.")
    body = json.dumps({
        "model": model,
        "max_tokens": 400,
        "messages": [{"role": "user", "content": question + "\n\nGive the answer first, then a short explanation."}],
    }).encode()
    request = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={"x-api-key": api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=60) as reply:
        data = json.load(reply)
    return "".join(block.get("text", "") for block in data.get("content", []))


def run_live(questions: list[dict[str, Any]], model: str) -> list[dict[str, Any]]:
    today = datetime.date.today().isoformat()
    rows = []
    for q in questions:
        print(f"asking {model}: {q['id']}")
        rows.append({"question_id": q["id"], "model": model, "date": today,
                     "source_type": "live_api_no_search", "response": ask_anthropic(q["question"], model)})
    out = ROOT / "responses" / f"live_{model}_{today}.jsonl"
    with open(out, "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"saved {out.relative_to(ROOT)}")
    return rows


def model_name(row: dict[str, Any]) -> str:
    return row["model"]


def excerpt(text: str, limit: int = 220) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[:limit].rstrip() + "..."


def build_report(questions: list[dict[str, Any]], results: list[dict[str, Any]],
                 response_files: list[pathlib.Path]) -> str:
    by_id = {q["id"]: q for q in questions}
    models = sorted({r["model"] for r in results})
    lines = [
        "# evalkit report",
        "",
        f"Generated {datetime.datetime.now():%Y-%m-%d %H:%M} from {len(questions)} questions and "
        f"{len(results)} responses ({', '.join(pathlib.Path(f).name for f in response_files)}).",
        "",
        "## Summary by model",
        "",
        "| Model | Responses | Score | " + " | ".join(LABELS) + " |",
        "| --- | --- | --- | " + " | ".join("---" for _ in LABELS) + " |",
    ]
    for m in models:
        rows = [r for r in results if r["model"] == m]
        score = sum(r["points"] for r in rows) / len(rows)
        counts = [str(sum(r["label"] == label for r in rows)) for label in LABELS]
        lines.append(f"| {m} | {len(rows)} | {score:.0%} | " + " | ".join(counts) + " |")

    labelled = [r for r in results if r.get("human_label")]
    if labelled:
        agree = sum(r["label"] == r["human_label"] for r in labelled)
        lines += ["", "## Automatic scorer vs human labels", "",
                  f"The automatic label matched the human label on {agree} of {len(labelled)} hand-labelled responses.", ""]
        for r in labelled:
            mark = "match" if r["label"] == r["human_label"] else "MISMATCH"
            lines.append(f"- **{r['question_id']} / {r['model']}:** auto `{r['label']}`, human `{r['human_label']}` ({mark}). {r.get('human_note', '')}")

    lines += ["", "## Failures in detail", ""]
    failures = [r for r in results if r["label"] != "correct"]
    if not failures:
        lines.append("No failures.")
    for r in failures:
        q = by_id[r["question_id"]]
        flags = ", ".join(r["flags"]) or "none"
        lines += [
            f"### {r['question_id']} / {r['model']}: `{r['label']}`",
            "",
            f"**Question:** {q['question']}",
            "",
            f"**Golden answer:** {q['answer']}  ",
            f"**Model said:** {excerpt(r['response'])}  ",
            f"**Flags:** {flags}",
            "",
            "**Evidence:**",
        ]
        for s in q["sources"]:
            lines.append(f"- [{s['title']}]({s['url']}): \"{s['quote']}\"")
        if q.get("notes"):
            lines.append(f"\n*Note:* {q['notes']}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--questions", default=ROOT / "data" / "questions.jsonl")
    parser.add_argument("--responses", action="append", help="responses JSONL file (repeatable)")
    parser.add_argument("--live", action="store_true", help="ask a model via the Anthropic API first")
    parser.add_argument("--model", default="claude-sonnet-5-5")
    parser.add_argument("--out", default=ROOT / "reports")
    args = parser.parse_args()

    questions = load_jsonl(args.questions)
    by_id = {q["id"]: q for q in questions}

    response_files = args.responses or ([] if args.live else DEFAULT_RESPONSES)
    responses = [row for f in response_files for row in load_jsonl(f)]
    if args.live:
        responses += run_live(questions, args.model)
        response_files = [*response_files, f"live:{args.model}"]

    results = []
    for row in responses:
        q = by_id.get(row["question_id"])
        if q is None:
            print(f"skipping unknown question id {row['question_id']}")
            continue
        results.append({**row, **score_response(q, row["response"])})

    out = pathlib.Path(args.out)
    out.mkdir(exist_ok=True)
    with open(out / "results.csv", "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["question_id", "model", "source_type", "label", "points", "flags", "human_label"])
        for r in results:
            writer.writerow([r["question_id"], r["model"], r.get("source_type", ""), r["label"],
                             r["points"], ";".join(r["flags"]), r.get("human_label", "")])
    (out / "report.md").write_text(build_report(questions, results, response_files), encoding="utf-8")

    print(f"Scored {len(results)} responses. Report: {out / 'report.md'}")
    for m in sorted({r['model'] for r in results}):
        rows = [r for r in results if r["model"] == m]
        print(f"  {m}: {sum(r['points'] for r in rows) / len(rows):.0%} over {len(rows)} responses")


if __name__ == "__main__":
    main()
