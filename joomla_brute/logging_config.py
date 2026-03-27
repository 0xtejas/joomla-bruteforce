"""Verbosity-aware logging setup."""

from __future__ import annotations

import logging
import sys


def configure_logging(verbosity: int) -> None:
    if verbosity >= 2:
        level = logging.DEBUG
    elif verbosity >= 1:
        level = logging.INFO
    else:
        level = logging.WARNING

    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
        stream=sys.stderr,
    )
    if verbosity >= 3:
        logging.getLogger("urllib3.connectionpool").setLevel(logging.DEBUG)
