from __future__ import annotations

import unittest

from lfsweaver.manifest import ManifestError, parse_manifest


def base_manifest() -> dict:
    return {
        "schema_version": 1,
        "project": {"name": "test"},
        "upstream": {
            "family": "lfs",
            "version": "13.0",
            "channel": "stable",
            "init": "systemd",
        },
        "target": {
            "architecture": "x86_64",
            "profile": "minimal",
            "outputs": ["rootfs"],
        },
        "executor": {"kind": "docker", "privileged": False},
        "verification": {"boot": False},
    }


class ManifestTests(unittest.TestCase):
    def test_valid_current_manifest(self) -> None:
        manifest = parse_manifest(base_manifest())
        self.assertEqual(manifest.upstream.version, "13.0")
        self.assertEqual(manifest.target.outputs, ("rootfs",))
        self.assertEqual(len(manifest.digest()), 64)

    def test_current_sysv_is_rejected(self) -> None:
        data = base_manifest()
        data["upstream"]["init"] = "sysv"
        with self.assertRaisesRegex(ManifestError, "last coordinated SysV release is 12.4"):
            parse_manifest(data)

    def test_legacy_sysv_lane_is_valid(self) -> None:
        data = base_manifest()
        data["upstream"].update(
            {"version": "12.4", "channel": "pinned", "init": "sysv", "book_commit": "12.4"}
        )
        manifest = parse_manifest(data)
        self.assertEqual(manifest.upstream.init, "sysv")

    def test_mlfs_i386_is_rejected(self) -> None:
        data = base_manifest()
        data["upstream"]["family"] = "mlfs"
        data["target"]["architecture"] = "i386"
        with self.assertRaisesRegex(ManifestError, "does not support i386"):
            parse_manifest(data)

    def test_kubernetes_i386_is_rejected(self) -> None:
        data = base_manifest()
        data["target"]["architecture"] = "i386"
        data["target"]["outputs"] = ["rootfs", "rke2"]
        with self.assertRaisesRegex(ManifestError, "require the x86_64"):
            parse_manifest(data)

    def test_iso_requires_install_verification(self) -> None:
        data = base_manifest()
        data["target"]["outputs"] = ["iso"]
        with self.assertRaisesRegex(ManifestError, "verification.install=true"):
            parse_manifest(data)

    def test_patch_requires_sha256(self) -> None:
        data = base_manifest()
        data["upstream"]["patches"] = [{"url": "https://example.test/fix.patch", "sha256": "bad"}]
        with self.assertRaisesRegex(ManifestError, "64 hex"):
            parse_manifest(data)

    def test_unknown_key_fails_closed(self) -> None:
        data = base_manifest()
        data["target"]["archtecture"] = "x86_64"
        with self.assertRaisesRegex(ManifestError, "unknown target keys: archtecture"):
            parse_manifest(data)


if __name__ == "__main__":
    unittest.main()
