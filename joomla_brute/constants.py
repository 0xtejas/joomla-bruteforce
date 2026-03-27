"""Shared constants for HTTP form fields and terminal styling."""

from __future__ import annotations


class BColors:
    """ANSI escape sequences (optional; disable via --no-color or NO_COLOR)."""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


DEFAULT_TIMEOUT_S = 30.0
RETURN_B64 = "aW5kZXgucGhw"
OPTION = "com_login"
TASK = "login"
USER_AGENT = "nano"
