"""Controller and worker prerequisite inspection."""

from __future__ import annotations

import platform
import shutil
import sys
from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Check:
    name: str
    status: str
    detail: str


def run_doctor(executor: str | None = None) -> dict[str, Any]:
    system = platform.system().lower()
    checks: list[Check] = [
        Check("python", "pass" if sys.version_info >= (3, 11) else "fail", platform.python_version()),
        Check("git", "pass" if shutil.which("git") else "fail", shutil.which("git") or "not found"),
    ]

    if executor in (None, "local"):
        checks.append(
            Check(
                "native-linux-worker",
                "pass" if system == "linux" else "fail",
                "LFS compilation needs a Linux kernel; use a VM, container, or SSH worker" if system != "linux" else platform.release(),
            )
        )
    if executor in (None, "docker"):
        checks.append(Check("docker", "pass" if shutil.which("docker") else "warn", shutil.which("docker") or "not found"))
    if executor in (None, "podman"):
        checks.append(Check("podman", "pass" if shutil.which("podman") else "warn", shutil.which("podman") or "not found"))
    if executor in (None, "ssh"):
        checks.append(Check("ssh", "pass" if shutil.which("ssh") else "warn", shutil.which("ssh") or "not found"))
    if executor in (None, "qemu"):
        qemu = shutil.which("qemu-system-x86_64") or shutil.which("qemu-system-i386")
        checks.append(Check("qemu", "pass" if qemu else "warn", qemu or "not found"))

    return {
        "controller_os": system,
        "controller_arch": platform.machine().lower(),
        "checks": [asdict(check) for check in checks],
        "ok": not any(check.status == "fail" for check in checks),
    }
