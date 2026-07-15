# Verification contract

## Pull-request gates

- manifest/provider schema tests;
- parser fixtures and semantic-diff snapshots;
- deterministic-plan tests;
- source URL and checksum validation;
- destructive-device selection tests;
- shell, workflow, and security linting once worker scripts land.

## Nightly gates

- clean LFS rootfs from a fully disposable worker;
- upstream test suites with a reviewed expected-failure allowlist;
- offline build after the fetch phase;
- OCI smoke tests;
- development and release-candidate canaries.

## Release gates

- two independent builds;
- SPDX and CycloneDX SBOMs;
- source/package/license inventory;
- vulnerability scan and checksums;
- in-toto/SLSA provenance and signatures;
- QEMU SeaBIOS and OVMF boot where applicable;
- ISO boot, install, eject, reboot, and smoke test;
- Docker, Podman, and containerd OCI tests.

## Cluster-node gates

K3s and RKE2 lanes use one-node and three-node x86_64 systemd VMs and test:

- node readiness and CoreDNS;
- CNI pod-to-pod and Service routing;
- local storage/PVC lifecycle;
- workload deployment;
- reboot and cluster rejoin.

Passing these tests means “LFSWeaver-verified,” not Rancher or vendor certified.

## Required report fields

Every report contains the project commit, all upstream refs, worker identity,
target/init/output, exact tests and results, duration, log locations, artifact
SHA-256, and SBOM/provenance locations.
