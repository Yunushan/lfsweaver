"""Project-wide constants and compatibility constraints."""

from __future__ import annotations

SCHEMA_VERSION = 1

BOOK_FAMILIES = ("lfs", "blfs", "mlfs", "glfs", "slfs")
INIT_SYSTEMS = ("systemd", "sysv")
ARCHITECTURES = ("i386", "x86_64")
OUTPUTS = ("rootfs", "oci", "docker", "raw", "iso", "k3s", "rke2")
EXECUTORS = ("local", "docker", "podman", "qemu", "ssh")
ENGINES = ("jhalfs", "native")
CHANNELS = ("stable", "development", "rc", "pinned")
EVIDENCE_STATES = ("verified", "tested", "experimental", "planned", "unsupported")

# These are upstream compatibility facts, not project marketing claims.
# A missing combination must remain experimental or unsupported until an adapter
# and public evidence exist.
UPSTREAM_COMPATIBILITY: dict[str, dict[str, object]] = {
    "lfs": {
        "current": "13.0",
        "current_inits": ("systemd",),
        "legacy_sysv": "12.4",
        "architectures": ("i386", "x86_64"),
    },
    "blfs": {
        "current": "13.0",
        "current_inits": ("systemd",),
        "legacy_sysv": "12.4",
        "architectures": ("i386", "x86_64"),
    },
    "mlfs": {
        "current": "13.0",
        "current_inits": ("systemd",),
        "legacy_sysv": None,
        "architectures": ("x86_64",),
    },
    "glfs": {
        "current": "13.0",
        "current_inits": ("systemd",),
        "legacy_sysv": None,
        "architectures": ("x86_64",),
    },
    "slfs": {
        "current": "13.0",
        "current_inits": ("systemd",),
        "legacy_sysv": None,
        "architectures": ("x86_64",),
    },
}

UPSTREAM_NEWS = {
    "lfs": "https://www.linuxfromscratch.org/lfs/news.html",
    "blfs": "https://www.linuxfromscratch.org/blfs/news.html",
    "mlfs": "https://www.linuxfromscratch.org/mlfs/news.html",
    "glfs": "https://www.linuxfromscratch.org/glfs/news.html",
    "slfs": "https://www.linuxfromscratch.org/slfs/news.html",
}
