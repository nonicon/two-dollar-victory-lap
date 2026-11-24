#!/usr/bin/env python3
"""Two-Dollar Victory Lap — a one-line roast of my own AI agent.

The entry is a single line of at most 200 characters, written to
/output/entry.txt. It is a constant string: the program is fully
deterministic and needs no input, no network and no secrets.

The entry is validated against the kit gate (1–200 UTF-8 characters,
single line, not only whitespace) before it is written, and the written
file is read back to confirm it is byte-for-byte identical to the
validated line. The output location honours MAKEFUN_OUTPUT_DIR first,
then OUTPUT_PATH, then /output/entry.txt.
"""

import os
import sys

ROAST = "My agent won $2 last month and celebrated so hard the compute cost $6."


def validate_entry(text: str) -> str:
    """Enforce the kit gate on the entry line, raising a clear error.
    Surrounding whitespace is stripped first, so the validated line is
    exactly what gets written — callers need not pre-strip."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    text = text.strip()
    text.encode("utf-8")  # must be valid UTF-8
    if not (1 <= len(text) <= 200):
        raise ValueError(f"entry is {len(text)} chars, must be 1-200")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def output_path() -> str:
    """Resolve where entry.txt goes: MAKEFUN_OUTPUT_DIR, else OUTPUT_PATH,
    else the default /output/entry.txt."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        return os.path.join(out_dir, "entry.txt")
    return os.environ.get("OUTPUT_PATH", "/output/entry.txt")


def main() -> int:
    text = validate_entry(ROAST.strip())
    path = output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    # Round-trip: the written file must be byte-for-byte the validated
    # line plus the trailing newline, so a truncated write never slips.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != text + "\n":
        print("round-trip mismatch: written file differs from entry",
              file=sys.stderr)
        return 1
    print(f"wrote {path} ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
