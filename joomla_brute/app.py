"""CLI entry: validate args, build session, run engine."""

from __future__ import annotations

import logging
import os
import sys

import requests

from joomla_brute.cli import parse_args
from joomla_brute.engine import run_bruteforce
from joomla_brute.fileio import iter_nonempty_lines
from joomla_brute.logging_config import configure_logging
from joomla_brute.session import build_session, fetch_initial_cookies
from joomla_brute.url_utils import normalize_admin_url, parse_proxy

LOG = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    configure_logging(args.verbose)

    use_color = not args.no_color and sys.stdout.isatty() and not os.environ.get("NO_COLOR")

    try:
        admin_url = normalize_admin_url(args.url)
    except Exception as e:
        LOG.error("Bad URL: %s", e)
        return 1

    proxies: dict[str, str] | None = None
    if args.proxy:
        try:
            proxies = parse_proxy(args.proxy)
        except ValueError as e:
            LOG.error("%s", e)
            return 1

    wordlist = args.wordlist
    if not wordlist.is_file():
        LOG.error("Wordlist not found: %s", wordlist)
        return 1

    if args.userlist is not None:
        ulist = args.userlist
        if not ulist.is_file():
            LOG.error("User list not found: %s", ulist)
            return 1
        usernames = list(iter_nonempty_lines(ulist))
    else:
        usernames = [args.username] if args.username else []

    if not usernames:
        LOG.error("No usernames to try")
        return 1

    if args.threads < 1:
        LOG.error("--threads must be >= 1")
        return 1

    session = build_session(proxies)
    try:
        fetch_initial_cookies(session, admin_url)
    except requests.RequestException as e:
        LOG.error("Failed to reach %s: %s", admin_url, e)
        return 1

    log_failures = args.verbose >= 1
    show_progress = not args.no_progress
    found, _u, _p = run_bruteforce(
        admin_url,
        wordlist,
        usernames,
        proxies=proxies,
        log_failures=log_failures,
        use_color=use_color,
        num_workers=args.threads,
        show_progress=show_progress,
    )
    if found:
        return 0
    LOG.warning("No valid credentials found")
    return 1
