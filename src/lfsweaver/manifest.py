"""TOML manifest loading and compatibility validation."""

from __future__ import annotations

import hashlib
import json
import re
import tomllib
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .constants import (
    ARCHITECTURES,
    BOOK_FAMILIES,
    CHANNELS,
    ENGINES,
    EXECUTORS,
    INIT_SYSTEMS,
    OUTPUTS,
    SCHEMA_VERSION,
    UPSTREAM_COMPATIBILITY,
)

_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class ManifestError(ValueError):
    """Raised when a manifest is malformed or requests an invalid combination."""


@dataclass(frozen=True)
class Project:
    name: str
    workspace: str = ".lfsweaver"


@dataclass(frozen=True)
class SourceRef:
    url: str
    sha256: str


@dataclass(frozen=True)
class Upstream:
    family: str
    version: str
    channel: str
    init: str
    book_commit: str = ""
    hints: tuple[str, ...] = ()
    patches: tuple[SourceRef, ...] = ()


@dataclass(frozen=True)
class Target:
    architecture: str
    profile: str
    outputs: tuple[str, ...]
    hostname: str = "lfsweaver"


@dataclass(frozen=True)
class Executor:
    kind: str
    endpoint: str = ""
    image: str = ""
    privileged: bool = False


@dataclass(frozen=True)
class Engine:
    kind: str = "jhalfs"
    ref: str = ""
    config_file: str = ""


@dataclass(frozen=True)
class Verification:
    package_tests: bool = True
    boot: bool = True
    install: bool = False
    reproducible: bool = False
    sbom: bool = True
    provenance: bool = True


@dataclass(frozen=True)
class Manifest:
    schema_version: int
    project: Project
    upstream: Upstream
    target: Target
    executor: Executor
    engine: Engine = field(default_factory=Engine)
    verification: Verification = field(default_factory=Verification)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    def digest(self) -> str:
        payload = json.dumps(
            self.as_dict(), sort_keys=True, separators=(",", ":"), ensure_ascii=True
        ).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()


def _table(data: dict[str, Any], name: str) -> dict[str, Any]:
    value = data.get(name)
    if not isinstance(value, dict):
        raise ManifestError(f"missing or invalid [{name}] table")
    return value


def _reject_unknown(table: dict[str, Any], allowed: set[str], label: str) -> None:
    unknown = sorted(set(table).difference(allowed))
    if unknown:
        raise ManifestError(f"unknown {label} keys: {', '.join(unknown)}")


def _text(table: dict[str, Any], key: str, *, default: str | None = None) -> str:
    value = table.get(key, default)
    if not isinstance(value, str) or not value.strip():
        raise ManifestError(f"{key} must be a non-empty string")
    return value.strip()


def _choice(value: str, choices: tuple[str, ...], label: str) -> str:
    if value not in choices:
        raise ManifestError(f"{label} must be one of: {', '.join(choices)}")
    return value


def _string_list(table: dict[str, Any], key: str) -> tuple[str, ...]:
    value = table.get(key, [])
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ManifestError(f"{key} must be an array of strings")
    return tuple(item.strip() for item in value if item.strip())


def _patches(table: dict[str, Any]) -> tuple[SourceRef, ...]:
    values = table.get("patches", [])
    if not isinstance(values, list):
        raise ManifestError("upstream.patches must be an array of tables")
    result: list[SourceRef] = []
    for index, value in enumerate(values):
        if not isinstance(value, dict):
            raise ManifestError(f"upstream.patches[{index}] must be a table")
        _reject_unknown(value, {"url", "sha256"}, f"upstream.patches[{index}]")
        url = _text(value, "url")
        sha256 = _text(value, "sha256").lower()
        if not _SHA256.fullmatch(sha256):
            raise ManifestError(f"upstream.patches[{index}].sha256 must be 64 hex characters")
        if not url.startswith("https://"):
            raise ManifestError(f"upstream.patches[{index}].url must use HTTPS")
        result.append(SourceRef(url=url, sha256=sha256))
    return tuple(result)


def _verification(table: dict[str, Any] | None) -> Verification:
    table = table or {}
    if not isinstance(table, dict):
        raise ManifestError("[verification] must be a table")
    _reject_unknown(
        table,
        {"package_tests", "boot", "install", "reproducible", "sbom", "provenance"},
        "verification",
    )

    def flag(key: str, default: bool) -> bool:
        value = table.get(key, default)
        if not isinstance(value, bool):
            raise ManifestError(f"verification.{key} must be true or false")
        return value

    return Verification(
        package_tests=flag("package_tests", True),
        boot=flag("boot", True),
        install=flag("install", False),
        reproducible=flag("reproducible", False),
        sbom=flag("sbom", True),
        provenance=flag("provenance", True),
    )


def _validate_compatibility(manifest: Manifest) -> None:
    upstream = manifest.upstream
    target = manifest.target
    facts = UPSTREAM_COMPATIBILITY[upstream.family]
    current = str(facts["current"])
    current_inits = tuple(facts["current_inits"])
    legacy_sysv = facts["legacy_sysv"]
    architectures = tuple(facts["architectures"])

    if target.architecture not in architectures:
        raise ManifestError(
            f"{upstream.family} {upstream.version} does not support "
            f"{target.architecture}; upstream architectures: {', '.join(architectures)}"
        )

    if upstream.version == current and upstream.init not in current_inits:
        legacy = f"; the last coordinated SysV release is {legacy_sysv}" if legacy_sysv else ""
        raise ManifestError(
            f"{upstream.family} {current} is {', '.join(current_inits)} only{legacy}"
        )

    if upstream.init == "sysv" and upstream.version != legacy_sysv:
        raise ManifestError(
            f"{upstream.family} SysV is only modeled as the pinned {legacy_sysv} lane"
        )

    node_outputs = {"k3s", "rke2"}.intersection(target.outputs)
    if node_outputs and (target.architecture != "x86_64" or upstream.init != "systemd"):
        raise ManifestError(
            "k3s/rke2 node images require the x86_64 + systemd lane; i386 is unsupported upstream"
        )

    if "iso" in target.outputs and not manifest.verification.install:
        raise ManifestError(
            "ISO output requires verification.install=true so CI must test install, eject, and reboot"
        )

    if manifest.executor.kind == "ssh" and not manifest.executor.endpoint:
        raise ManifestError("executor.endpoint is required for the ssh executor")

    if manifest.upstream.channel == "pinned" and not manifest.upstream.book_commit:
        raise ManifestError("upstream.book_commit is required for channel=pinned")


def parse_manifest(data: dict[str, Any]) -> Manifest:
    _reject_unknown(
        data,
        {"schema_version", "project", "upstream", "target", "executor", "engine", "verification"},
        "top-level",
    )
    schema_version = data.get("schema_version")
    if schema_version != SCHEMA_VERSION:
        raise ManifestError(f"schema_version must be {SCHEMA_VERSION}")

    project_data = _table(data, "project")
    upstream_data = _table(data, "upstream")
    target_data = _table(data, "target")
    executor_data = _table(data, "executor")

    _reject_unknown(project_data, {"name", "workspace"}, "project")
    _reject_unknown(
        upstream_data,
        {"family", "version", "channel", "init", "book_commit", "hints", "patches"},
        "upstream",
    )
    _reject_unknown(target_data, {"architecture", "profile", "outputs", "hostname"}, "target")
    _reject_unknown(executor_data, {"kind", "endpoint", "image", "privileged"}, "executor")

    project = Project(
        name=_text(project_data, "name"),
        workspace=_text(project_data, "workspace", default=".lfsweaver"),
    )
    upstream = Upstream(
        family=_choice(_text(upstream_data, "family"), BOOK_FAMILIES, "upstream.family"),
        version=_text(upstream_data, "version"),
        channel=_choice(_text(upstream_data, "channel", default="stable"), CHANNELS, "upstream.channel"),
        init=_choice(_text(upstream_data, "init"), INIT_SYSTEMS, "upstream.init"),
        book_commit=str(upstream_data.get("book_commit", "")).strip(),
        hints=_string_list(upstream_data, "hints"),
        patches=_patches(upstream_data),
    )
    outputs = _string_list(target_data, "outputs")
    if not outputs:
        raise ManifestError("target.outputs must contain at least one output")
    unknown_outputs = sorted(set(outputs).difference(OUTPUTS))
    if unknown_outputs:
        raise ManifestError(f"unknown target outputs: {', '.join(unknown_outputs)}")
    if len(set(outputs)) != len(outputs):
        raise ManifestError("target.outputs must not contain duplicates")
    target = Target(
        architecture=_choice(_text(target_data, "architecture"), ARCHITECTURES, "target.architecture"),
        profile=_text(target_data, "profile", default="minimal"),
        outputs=outputs,
        hostname=_text(target_data, "hostname", default="lfsweaver"),
    )
    executor = Executor(
        kind=_choice(_text(executor_data, "kind"), EXECUTORS, "executor.kind"),
        endpoint=str(executor_data.get("endpoint", "")).strip(),
        image=str(executor_data.get("image", "")).strip(),
        privileged=bool(executor_data.get("privileged", False)),
    )
    if not isinstance(executor_data.get("privileged", False), bool):
        raise ManifestError("executor.privileged must be true or false")

    engine_data = data.get("engine", {})
    if not isinstance(engine_data, dict):
        raise ManifestError("[engine] must be a table")
    _reject_unknown(engine_data, {"kind", "ref", "config_file"}, "engine")
    engine = Engine(
        kind=_choice(_text(engine_data, "kind", default="jhalfs"), ENGINES, "engine.kind"),
        ref=str(engine_data.get("ref", "")).strip(),
        config_file=str(engine_data.get("config_file", "")).strip(),
    )

    manifest = Manifest(
        schema_version=schema_version,
        project=project,
        upstream=upstream,
        target=target,
        executor=executor,
        engine=engine,
        verification=_verification(data.get("verification")),
    )
    _validate_compatibility(manifest)
    return manifest


def load_manifest(path: str | Path) -> Manifest:
    manifest_path = Path(path)
    try:
        with manifest_path.open("rb") as handle:
            data = tomllib.load(handle)
    except FileNotFoundError as exc:
        raise ManifestError(f"manifest not found: {manifest_path}") from exc
    except tomllib.TOMLDecodeError as exc:
        raise ManifestError(f"invalid TOML in {manifest_path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ManifestError("manifest root must be a table")
    return parse_manifest(data)
