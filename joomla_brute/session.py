"""HTTP session factory and timed request helpers."""

from __future__ import annotations

import logging
from typing import Any

import requests
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from joomla_brute.constants import DEFAULT_TIMEOUT_S, USER_AGENT

LOG = logging.getLogger(__name__)


def build_session(proxies: dict[str, str] | None) -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    if proxies:
        session.proxies.update(proxies)

    retries = Retry(
        total=3,
        backoff_factor=0.3,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET", "POST"),
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def session_get(session: requests.Session, url: str, **kwargs: Any) -> Response:
    kwargs.setdefault("timeout", DEFAULT_TIMEOUT_S)
    return session.get(url, **kwargs)


def session_post(session: requests.Session, url: str, **kwargs: Any) -> Response:
    kwargs.setdefault("timeout", DEFAULT_TIMEOUT_S)
    return session.post(url, **kwargs)


def fetch_initial_cookies(session: requests.Session, admin_url: str) -> None:
    r = session_get(session, admin_url)
    r.raise_for_status()
    LOG.debug("Initial GET %s -> %s", admin_url, r.status_code)
