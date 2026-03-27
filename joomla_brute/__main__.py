"""Allow `python -m joomla_brute`."""

from __future__ import annotations

import sys

from joomla_brute.app import main

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
