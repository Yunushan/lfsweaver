# Architecture

LFSWeaver separates portable control, privileged build execution, artifact
composition, and verification. This prevents a successful controller smoke
test from being misreported as a successful LFS build.

## Layers

1. **Controller** — loads and validates the stable manifest, resolves providers,
   creates an immutable plan, selects a worker, and gathers reports.
2. **Provider** — translates a pinned upstream book/release into normalized
   steps. Providers are declarative data or versioned subprocesses speaking a
   JSON protocol; platform-specific in-process plugins are avoided.
3. **Linux worker** — executes build steps in a disposable VM or dedicated
   remote host. Container execution may be offered for convenience, but a
   privileged container is not treated as isolation.
4. **Composer** — converts a rootfs into an OCI archive, raw disk, installer
   ISO, or cluster-node system.
5. **Verifier** — runs package, chroot, QEMU, installation, OCI-runtime,
   reproducibility, and Kubernetes tests.
6. **Evidence publisher** — binds reports, logs, upstream locks, artifact
   digests, SBOMs, and provenance to a capability claim.

## Stable contracts

- `schema_version` protects manifest compatibility.
- A provider consumes a manifest plus an immutable upstream lock and emits a
  normalized JSON plan.
- Plans are deterministic and content-addressed.
- Every executed step emits a machine-readable report.
- Evidence promotion is separate from build execution and fails closed.

## Security boundaries

The controller is unprivileged. Mounting, loop devices, chroot, bootloader
installation, and raw-disk writes belong exclusively to the disposable Linux
worker. Secrets are injected at execution time and must never appear in plans,
logs, manifests, images, or provenance.

## Reproducibility boundary

Bit-for-bit reproducibility is evaluated only after normalizing known volatile
metadata. If exact equality is impossible, the report must identify each
difference and the claim remains below `verified` until an explicit policy is
approved.
