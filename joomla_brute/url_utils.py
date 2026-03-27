"""URL normalization and proxy parsing."""

from __future__ import annotations

from urllib.parse import urljoin, urlparse


def normalize_admin_url(base: str) -> str:
    base = base.rstrip("/")
    return urljoin(base + "/", "administrator/")


def parse_proxy(proxy_url: str) -> dict[str, str]:
    """Build a requests-compatible proxies dict."""
    parsed = urlparse(proxy_url)
    if not parsed.scheme or not parsed.netloc:
        msg = f"Invalid proxy URL (need scheme and host): {proxy_url!r}"
        raise ValueError(msg)
    full = f"{parsed.scheme}://{parsed.netloc}"
    return {"http": full, "https": full}
