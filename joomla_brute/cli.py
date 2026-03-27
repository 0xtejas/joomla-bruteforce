"""Argument parsing for the Joomla brute-force CLI."""

from __future__ import annotations

import argparse
import os
from pathlib import Path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="joomla-brute",
        description="Joomla login bruteforce (administrator panel)",
    )
    parser.add_argument(
        "-u",
        "--url",
        required=True,
        help="Joomla site base URL (e.g. http://10.10.10.150)",
    )
    parser.add_argument(
        "-w",
        "--wordlist",
        required=True,
        type=Path,
        help="Path to password wordlist file",
    )
    parser.add_argument(
        "-p",
        "--proxy",
        help="HTTP(S) proxy, e.g. http://127.0.0.1:8080",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (-v info, -vv debug, -vvv trace)",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI colors in credential output",
    )
    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=max(4, min(32, (os.cpu_count() or 4) * 2)),
        metavar="N",
        help="Concurrent worker threads (each uses its own HTTP session; default: %(default)s)",
    )
    parser.add_argument(
        "--no-progress",
        action="store_true",
        help="Disable the tqdm progress bar",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-usr", "--username", help="Single username")
    group.add_argument("-U", "--userlist", type=Path, help="Username list file")

    return parser.parse_args(argv)
