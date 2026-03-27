#!/usr/bin/env python3
"""Backward-compatible entry point; prefer `uv run joomla-brute` or `python -m joomla_brute`."""

from joomla_brute import main

if __name__ == "__main__":
    raise SystemExit(main())
