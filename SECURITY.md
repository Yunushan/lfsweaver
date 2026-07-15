# Security policy

## Supported versions

Until the first stable release, security fixes are applied only to the latest
commit on `main`.

## Reporting a vulnerability

Use GitHub's private security-advisory reporting flow for this repository. Do
not open a public issue containing an exploit, secret, unsafe disk command, or
unpatched vulnerability details.

Include the affected commit, execution backend, target profile, reproduction
steps, impact, and a suggested mitigation if available.

## Threat model summary

LFS builds execute third-party configure scripts, Makefiles, package tests, and
book instructions. Treat all build input as untrusted. Use a disposable VM or a
dedicated worker with no production credentials or writable production mounts.
A privileged container does not provide a security boundary.

Raw-disk and installer code must never select a target by unstable `/dev/sdX`
name alone. Device identity, mount state, model, serial, size, and an explicit
allowlist are required before any write.
