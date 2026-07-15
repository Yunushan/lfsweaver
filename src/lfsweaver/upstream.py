"""Release discovery with intentionally conservative parsing."""

from __future__ import annotations

import re
import urllib.request
from dataclasses import dataclass

from .constants import BOOK_FAMILIES, UPSTREAM_NEWS


class UpstreamError(RuntimeError):
    pass


@dataclass(frozen=True)
class Release:
    family: str
    version: str
    source_url: str


def parse_latest_release(family: str, body: str) -> str:
    family = family.lower()
    if family not in BOOK_FAMILIES:
        raise UpstreamError(f"unknown family: {family}")
    pattern = re.compile(
        rf"\b{re.escape(family.upper())}[- ](\d+\.\d+)"
        rf"(?:\s+Release\b|\s+has\s+been\s+released\b)",
        re.IGNORECASE,
    )
    versions = pattern.findall(body)
    if not versions:
        raise UpstreamError(f"could not find a stable {family.upper()} release in upstream news")
    return max(versions, key=lambda value: tuple(int(part) for part in value.split(".")))


def check_release(family: str, *, timeout: float = 20.0) -> Release:
    family = family.lower()
    if family not in UPSTREAM_NEWS:
        raise UpstreamError(f"unknown family: {family}")
    url = UPSTREAM_NEWS[family]
    request = urllib.request.Request(url, headers={"User-Agent": "LFSWeaver/0.1 release-watch"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
    except OSError as exc:
        raise UpstreamError(f"failed to read {url}: {exc}") from exc
    return Release(family=family, version=parse_latest_release(family, body), source_url=url)
