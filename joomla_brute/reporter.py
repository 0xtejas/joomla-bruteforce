"""Human-readable credential output (stdout)."""

from __future__ import annotations

import threading

from joomla_brute.constants import BColors


def print_result(
    username: str,
    password: str,
    failed: bool,
    *,
    use_color: bool,
    lock: threading.Lock | None = None,
) -> None:
    def _emit() -> None:
        if use_color:
            if failed:
                print(f"{BColors.FAIL} {username}:{password}{BColors.ENDC}")
            else:
                print(f"{BColors.OKGREEN} {username}:{password}{BColors.ENDC}")
        else:
            print(f"{username}:{password}")

    if lock is not None:
        with lock:
            _emit()
    else:
        _emit()
