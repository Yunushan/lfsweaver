"""Deterministic build-plan generation."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from .manifest import Manifest


@dataclass(frozen=True)
class Step:
    id: str
    action: str
    requires: tuple[str, ...]
    evidence: str


@dataclass(frozen=True)
class BuildPlan:
    schema_version: int
    manifest_sha256: str
    family: str
    version: str
    init: str
    architecture: str
    executor: str
    engine: str
    steps: tuple[Step, ...]

    def as_dict(self, *, include_digest: bool = True) -> dict[str, Any]:
        data = asdict(self)
        if include_digest:
            data["plan_sha256"] = self.digest()
        return data

    def digest(self) -> str:
        data = self.as_dict(include_digest=False)
        payload = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()


def create_plan(manifest: Manifest) -> BuildPlan:
    steps: list[Step] = [
        Step("preflight", "validate controller and Linux worker", ("controller",), "preflight.json"),
        Step("lock", "resolve immutable upstream and package lock", ("network",), "source-lock.json"),
        Step("fetch", "fetch books, packages, hints, and allowlisted patches", ("network",), "fetch-report.json"),
        Step("source-verify", "verify every source checksum", (), "source-verification.json"),
        Step("book-plan", "normalize book instructions into the build IR", (), "book-plan.json"),
        Step(
            "build",
            f"execute book phases with the {manifest.engine.kind} engine in the disposable Linux worker",
            ("linux-worker",),
            "build-report.json",
        ),
    ]

    if manifest.upstream.family != "lfs":
        steps.append(
            Step(
                "extensions",
                f"apply curated {manifest.upstream.family.upper()} profile",
                ("linux-worker",),
                "extension-report.json",
            )
        )

    steps.append(Step("rootfs", "compose immutable root filesystem", ("linux-worker",), "rootfs-report.json"))

    for output in manifest.target.outputs:
        if output == "rootfs":
            continue
        requirements = ["linux-worker"]
        if output in {"raw", "iso"}:
            requirements.append("qemu")
        if output in {"oci", "docker"}:
            requirements.append("oci-runtime")
        if output in {"k3s", "rke2"}:
            requirements.extend(("qemu", "nested-virtualization"))
        steps.append(
            Step(
                f"compose-{output}",
                f"compose {output} artifact",
                tuple(requirements),
                f"{output}-compose-report.json",
            )
        )

    if manifest.verification.package_tests:
        steps.append(Step("package-tests", "evaluate upstream test suites", ("linux-worker",), "package-tests.json"))
    if manifest.verification.boot and set(manifest.target.outputs).intersection({"raw", "iso", "k3s", "rke2"}):
        steps.append(Step("boot-test", "boot artifact with firmware matrix", ("qemu",), "boot-test.json"))
    if manifest.verification.install and "iso" in manifest.target.outputs:
        steps.append(
            Step(
                "install-test",
                "install ISO to blank disk, eject media, reboot, and smoke test",
                ("qemu",),
                "install-test.json",
            )
        )
    if set(manifest.target.outputs).intersection({"k3s", "rke2"}):
        steps.append(
            Step(
                "cluster-test",
                "verify node readiness, DNS, CNI, storage, reboot, and rejoin",
                ("nested-virtualization",),
                "cluster-test.json",
            )
        )
    if manifest.verification.reproducible:
        steps.append(
            Step(
                "reproducibility",
                "perform independent rebuild and compare normalized artifacts",
                ("second-worker",),
                "reproducibility.json",
            )
        )
    if manifest.verification.sbom:
        steps.append(Step("sbom", "generate SPDX and CycloneDX inventories", (), "sbom-report.json"))
    if manifest.verification.provenance:
        steps.append(Step("attest", "emit checksums and in-toto provenance", (), "provenance.json"))

    return BuildPlan(
        schema_version=1,
        manifest_sha256=manifest.digest(),
        family=manifest.upstream.family,
        version=manifest.upstream.version,
        init=manifest.upstream.init,
        architecture=manifest.target.architecture,
        executor=manifest.executor.kind,
        engine=manifest.engine.kind,
        steps=tuple(steps),
    )
