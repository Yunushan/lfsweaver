"""Command-line interface for the cross-platform controller."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from . import __version__
from .doctor import run_doctor
from .evidence import EvidenceError, load_evidence
from .manifest import ManifestError, load_manifest
from .plan import create_plan
from .upstream import UpstreamError, check_release

DEFAULT_TEMPLATE = """schema_version = 1

[project]
name = "my-lfs-system"
workspace = ".lfsweaver"

[upstream]
family = "lfs"
version = "13.0"
channel = "stable"
init = "systemd"
hints = []
patches = []

[target]
architecture = "x86_64"
profile = "minimal"
outputs = ["rootfs"]
hostname = "lfsweaver"

[executor]
kind = "docker"
image = "ubuntu:24.04"
privileged = false

[engine]
kind = "jhalfs"

[verification]
package_tests = true
boot = false
install = false
reproducible = false
sbom = true
provenance = true
"""


def _json(data: object) -> None:
    print(json.dumps(data, indent=2, sort_keys=True))


def _cmd_init(args: argparse.Namespace) -> int:
    destination = Path(args.path)
    if destination.exists() and not args.force:
        raise ManifestError(f"refusing to overwrite {destination}; pass --force")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(DEFAULT_TEMPLATE, encoding="utf-8")
    print(f"created {destination}")
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    manifest = load_manifest(args.manifest)
    result = {
        "valid": True,
        "manifest": str(Path(args.manifest)),
        "manifest_sha256": manifest.digest(),
        "family": manifest.upstream.family,
        "version": manifest.upstream.version,
        "init": manifest.upstream.init,
        "architecture": manifest.target.architecture,
        "outputs": list(manifest.target.outputs),
    }
    if args.json:
        _json(result)
    else:
        print(
            f"valid: {result['family']} {result['version']} {result['init']} "
            f"{result['architecture']} -> {', '.join(result['outputs'])}"
        )
        print(f"manifest sha256: {result['manifest_sha256']}")
    return 0


def _cmd_plan(args: argparse.Namespace) -> int:
    plan = create_plan(load_manifest(args.manifest))
    data = plan.as_dict()
    output = json.dumps(data, indent=2, sort_keys=True) + "\n"
    if args.output:
        destination = Path(args.output)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(output, encoding="utf-8")
        print(f"wrote {destination}")
    else:
        print(output, end="")
    return 0


def _cmd_doctor(args: argparse.Namespace) -> int:
    result = run_doctor(args.executor)
    if args.json:
        _json(result)
    else:
        print(f"controller: {result['controller_os']}/{result['controller_arch']}")
        for check in result["checks"]:
            print(f"{check['status']:>4}  {check['name']}: {check['detail']}")
    return 0 if result["ok"] else 1


def _cmd_evidence(args: argparse.Namespace) -> int:
    data = load_evidence(args.path)
    counts: dict[str, int] = {}
    for claim in data["claims"]:
        counts[claim["state"]] = counts.get(claim["state"], 0) + 1
    result = {"valid": True, "claims": len(data["claims"]), "states": counts}
    if args.json:
        _json(result)
    else:
        print(f"valid evidence ledger: {result['claims']} claims")
        for state, count in sorted(counts.items()):
            print(f"  {state}: {count}")
    return 0


def _cmd_release(args: argparse.Namespace) -> int:
    release = check_release(args.family, timeout=args.timeout)
    result = {"family": release.family, "version": release.version, "source_url": release.source_url}
    if args.json:
        _json(result)
    else:
        print(f"latest {release.family.upper()} release: {release.version}")
        print(release.source_url)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lfsweaver",
        description="Plan and verify evidence-backed Linux From Scratch builds.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="create a safe starter manifest")
    init.add_argument("path", nargs="?", default="lfsweaver.toml")
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=_cmd_init)

    validate = subparsers.add_parser("validate", help="validate a manifest and compatibility rules")
    validate.add_argument("manifest", nargs="?", default="lfsweaver.toml")
    validate.add_argument("--json", action="store_true")
    validate.set_defaults(func=_cmd_validate)

    plan = subparsers.add_parser("plan", help="emit a deterministic build plan")
    plan.add_argument("manifest", nargs="?", default="lfsweaver.toml")
    plan.add_argument("--output", "-o")
    plan.set_defaults(func=_cmd_plan)

    doctor = subparsers.add_parser("doctor", help="inspect controller and worker prerequisites")
    doctor.add_argument("--executor", choices=("local", "docker", "podman", "qemu", "ssh"))
    doctor.add_argument("--json", action="store_true")
    doctor.set_defaults(func=_cmd_doctor)

    evidence = subparsers.add_parser("evidence", help="validate the support-claim ledger")
    evidence.add_argument("path", nargs="?", default="evidence/support.json")
    evidence.add_argument("--json", action="store_true")
    evidence.set_defaults(func=_cmd_evidence)

    release = subparsers.add_parser("release", help="check official upstream release news")
    release.add_argument("family", choices=("lfs", "blfs", "mlfs", "glfs", "slfs"))
    release.add_argument("--timeout", type=float, default=20.0)
    release.add_argument("--json", action="store_true")
    release.set_defaults(func=_cmd_release)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (ManifestError, EvidenceError, UpstreamError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
