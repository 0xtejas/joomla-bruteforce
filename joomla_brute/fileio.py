"""Line-oriented file reading for wordlists."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path


def iter_nonempty_lines(path: Path, encoding: str = "utf-8") -> Iterator[str]:
    with path.open(encoding=encoding, errors="replace") as f:
        for line in f:
            s = line.strip()
            if s:
                yield s


def count_nonempty_lines(path: Path, encoding: str = "utf-8") -> int:
    n = 0
    with path.open(encoding=encoding, errors="replace") as f:
        for line in f:
            if line.strip():
                n += 1
    return n
