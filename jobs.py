"""
jobs.py — functions that the RQ worker executes.

Rules:
  1. Must be importable at the top level (no closures / lambdas).
  2. All arguments must be picklable (strings, dicts, numbers — not Flask objects).
  3. Raise exceptions freely; RQ catches them and marks the job as "failed".
"""

import time


def count_words(text: str) -> dict:
    """Simulate a slow job by sleeping, then count words."""
    time.sleep(3)                          # pretend this is real work
    words = text.split()
    return {
        "word_count": len(words),
        "char_count": len(text),
        "words": words,
    }