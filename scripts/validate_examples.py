#!/usr/bin/env python3
"""Validate every complete example manifest."""

from __future__ import annotations

from pathlib import Path

from lfsweaver.manifest import load_manifest
from lfsweaver.plan import create_plan


def main() -> int:
    examples = sorted(Path("examples").glob("*.toml"))
    if not examples:
        raise SystemExit("no example manifests found")
    for path in examples:
        manifest = load_manifest(path)
        plan = create_plan(manifest)
        print(f"valid {path}: {plan.digest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
