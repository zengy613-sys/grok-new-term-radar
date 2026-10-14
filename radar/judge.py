"""Is this term the name of a new thing, or a common word?

The free default (`judge.model` = "local") is a heuristic: it drops stop words, terms you
already cover (`known` on the row, set from config.json's known_terms), and common words,
and it suppresses long fine-tune titles (quantised copies, "uncensored", LoRA, and titles
long enough to be a model card rather than a name). No key, no network.

A paid model is still available: set `judge.model` to a chat model and provide an AIsa key.
One chat call per CHUNK terms. If that call fails the terms keep no score and the report
lists them all: the judge sorts the report, it never blocks it.
"""
from __future__ import annotations

import json
import re

from . import aisa
from .terms import STOP

CHUNK = 25
LOCAL = "local"
# Everyday words the signals still surface. A term made only of these (and stop words) is not a name.
COMMON = set("""
dashboard pricing today lots trained anatomy math iphone pdf notes voice generator release
blog guide tutorial download login search news update review reviews article articles
category popular trending latest official free online best app website image video audio
photo photos music file files user users account settings help support docs community
feature features version versions changelog about contact privacy cookie cookies menu
index list lists item items post posts tag tags topic topics general other misc default
custom basic advanced pro plus lite mini max ultra super home page
""".split())
# A long title that still carries one of these is a fine-tune or a quantised copy, not the name
# people search. Short names that merely contain a digit ("krea 2", "opus 5.5") are kept.
_FINE_TUNE = re.compile(
    r"\b(?:gguf|ggml|awq|gptq|fp8|fp16|bf16|int4|int8|mlx|exl2|onnx|uncensored|abliterated|"
    r"lora|qlora|finetune|finetuned|fine-?tuned?|quantized|quantised|imatrix|q\d[\w.]*)\b",
    re.I)
_NAME = 0.9
_COMMON = 0.15
_FINETUNE = 0.2
SYSTEM = (
    "You sort terms for a radar that looks for new product names. For each term, score from 0.0 to 1.0 how likely "
    "it is the NAME of one specific product, model, tool, library, company or technique, as opposed to a common "
    "word, a generic category, a feature description or a fragment of a sentence. `examples` are places where the "
    "term appeared (posts, repository descriptions, model ids, URL paths); use them.\n"
    "Names: 'opus 5.5', 'hyperframes', 'seedance', 'qwen image 2.1', 'strata' (when the examples show a project "
    "called Strata).\n"
    "Not names: 'dashboard', 'voice notes', 'pdf', 'lots', 'trained', 'video generator', 'new release', 'today'.\n"
    "A known company or product family alone ('google', 'claude') is a name, but an old one: score it 0.5.\n"
    "Answer with JSON only, one object per term, in the same order: [{\"i\": 0, \"score\": 0.9}, ...]"
)


def parse(answer: str, n: int) -> dict[int, float]:
    """{index: score} from the model's answer; indexes outside 0..n-1 and bad scores are dropped."""
    m = re.search(r"\[.*\]", answer, re.S)
    try:
        items = json.loads(m.group(0)) if m else []
    except ValueError:
        return {}
    out = {}
    for it in items if isinstance(items, list) else []:
        try:
            i, score = int(it["i"]), float(it["score"])
        except (KeyError, TypeError, ValueError):
            continue
        if 0 <= i < n and 0.0 <= score <= 1.0:
            out[i] = score
    return out


def long_finetune(term: str) -> bool:
    """A model-card title: six or more words, or four or more when it is a quantised copy or a fine-tune."""
    words = term.split()
    if len(words) >= 6:
        return True
    return len(words) >= 4 and bool(_FINE_TUNE.search(term))


def heuristic(row: dict) -> float:
    """0..1 with no model. Below the default min_score (0.5): stop words, known terms, common words, long fine-tunes."""
    term = " ".join(str(row.get("term") or "").lower().split())
    if not term or row.get("known"):
        return 0.0
    words = term.split()
    if all(w in STOP for w in words):
        return 0.0
    if all(w in STOP or w in COMMON for w in words):
        return _COMMON
    if long_finetune(term):
        return _FINETUNE
    return _NAME


def local_score(rows: list[dict]) -> dict:
    """The free judge. Sets r["named"] on every row. Returns {"judged": n, "local": True}."""
    for row in rows:
        row["named"] = heuristic(row)
    return {"judged": len(rows), "local": True}


def score(rows: list[dict], model: str) -> dict:
    """Sets r["named"] on each row the judge scored. Returns {"judged": n} or {"error": ...}.

    `model` "local" (the default) is the heuristic. An empty model skips scoring, which is
    what `--skip judge` asks for. Any other model is one paid chat call per chunk.
    """
    if model in {LOCAL, "heuristic"}:
        return local_score(rows)
    if not model:
        return {"judged": 0, "skipped": True}
    judged = 0
    for start in range(0, len(rows), CHUNK):
        chunk = rows[start:start + CHUNK]
        user = json.dumps([{"i": i, "term": r["term"], "examples": [e[:160] for e in r.get("examples", [])[:3]]}
                           for i, r in enumerate(chunk)], ensure_ascii=False)
        try:
            scores = parse(aisa.chat(model, SYSTEM, user), len(chunk))
        except aisa.AisaError as exc:
            return {"judged": judged, "error": str(exc)[:160]}
        for i, s in scores.items():
            chunk[i]["named"] = s
        judged += len(scores)
    return {"judged": judged}
