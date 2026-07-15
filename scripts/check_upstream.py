#!/usr/bin/env python3
"""Fail with a distinct code when upstream stable versions drift."""

from __future__ import annotations

import argparse
import json

from lfsweaver.constants import BOOK_FAMILIES, UPSTREAM_COMPATIBILITY
from lfsweaver.upstream import UpstreamError, check_release


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("family", choices=BOOK_FAMILIES)
    args = parser.parse_args()
    try:
        release = check_release(args.family)
    except UpstreamError as exc:
        print(json.dumps({"family": args.family, "error": str(exc)}, sort_keys=True))
        return 2
    modeled = str(UPSTREAM_COMPATIBILITY[args.family]["current"])
    result = {
        "family": args.family,
        "modeled": modeled,
        "upstream": release.version,
        "source_url": release.source_url,
        "drift": release.version != modeled,
    }
    print(json.dumps(result, sort_keys=True))
    return 10 if result["drift"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
