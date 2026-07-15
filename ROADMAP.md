# Roadmap

The roadmap is evidence-gated. A milestone is complete only when its artifacts
and test reports are public; merged templates alone do not count as support.

## P0 — contracts and guardrails (current)

- [x] Project identity and 0BSD license
- [x] Stable TOML manifest and deterministic build-plan model
- [x] Upstream compatibility constraints
- [x] Evidence ledger and proof validation
- [x] Cross-platform controller CI definition
- [x] Scheduled stable-release detection
- [x] Documentation, safety model, and reference parity audit

## P1 — first bootable system

- [ ] Versioned LFS and official jhalfs providers
- [ ] Immutable source/package/patch lock with SHA-256
- [ ] Disposable Linux VM executor
- [ ] LFS 13.0 systemd x86_64 rootfs
- [ ] OCI output tested on Docker, Podman, and containerd
- [ ] BIOS + UEFI raw disk with QEMU boot evidence
- [ ] Two-build reproducibility report, SBOM, and provenance
- [ ] Pinned LFS 12.4 SysV x86_64 lane

## P2 — installer, i386, and curated BLFS

- [ ] Installer ISO and install/eject/reboot E2E
- [ ] Blank physical/virtual disk deployment safety gates
- [ ] LFS 13.0 i386 rootfs and BIOS raw image
- [ ] BLFS 13.0 curated minimal, server, and XFCE profiles
- [ ] Windows/Windows Server WSL2 and Hyper-V controller adapters
- [ ] macOS VM/remote controller adapter

## P3 — extended LFS family

- [ ] MLFS 13.0 x86_64 multilib provider
- [ ] Curated GLFS and SLFS 13.0 profiles
- [ ] GPU-labeled and physical-hardware verification lanes
- [ ] Hints index and individually tested adapters
- [ ] Book-required/allowlisted patch catalog
- [ ] BSD, Solaris/illumos, and Android remote-controller lanes

## P4 — cluster-node systems

- [ ] K3s x86_64 systemd node image
- [ ] RKE2 x86_64 systemd node image
- [ ] One-node and three-node E2E for readiness, DNS, CNI, services, PVCs,
      workload deployment, reboot, and rejoin
- [ ] Remote web/API client usable from iOS

## Intentionally unsupported

- native local builds on stock iOS;
- K3s or RKE2 on i386;
- current GLFS/SLFS SysV variants that upstream no longer publishes;
- overwriting the currently mounted running root filesystem;
- universal application of every Hint and Patch;
- “forever compatible” auto-upgrades without semantic review;
- claims of vendor certification from project-owned integration tests.
