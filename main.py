#!/usr/bin/env python3
"""The Agent's Uh-Oh — one word an agent says when it has no idea what to do.

Writes the word to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output),
atomically, then re-reads it to verify the gate: UTF-8, 1-99 chars,
a single word, not only whitespace. Pure stdlib, deterministic, no network.
"""

import os
import sys

WORD = "hallucinating"


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    # Gate self-check before writing: one word, 1-99 chars, not blank.
    if not WORD or len(WORD) > 99 or WORD.strip() != WORD or len(WORD.split()) != 1:
        print(f"entry fails gate: {WORD!r}", file=sys.stderr)
        return 1

    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(WORD)
    os.replace(tmp, path)

    # Re-read and verify the bytes on disk.
    with open(path, "rb") as f:
        data = f.read()
    text = data.decode("utf-8")
    if text != WORD or not 1 <= len(text) <= 99 or len(text.split()) != 1:
        print(f"verification failed: {data!r}", file=sys.stderr)
        return 1
    print(f"wrote {len(text)} chars to {path}: {text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
