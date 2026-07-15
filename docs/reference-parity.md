# Reference-project parity

This table is pinned to the projects audited on 2026-07-15. “Planned” is not a
claim that a working implementation already exists.

| Reference | Useful behavior | LFSWeaver mapping | State |
|---|---|---|---|
| `eliaz5536/LFSInstaller` | release catalogs, checksums, single/four-phase generation | provider locks and normalized phases | Contract implemented; worker planned |
| `KeithDHedger/LFSDesktopProject` | lightweight X11 desktop suite | optional curated BLFS desktop profile; external GPL component | Planned |
| `lumenthi/Linux-From-Scratch` | explicit disk, kernel, GRUB walkthrough | raw composer and boot reports without hard-coded devices | Planned |
| `luisgbm/lfs-scripts` | four phases and logs | deterministic step graph and per-step reports | Planner implemented; worker planned |
| `reinterpretcat/lfs` | isolated build, rootfs/ramdisk/ISO stages | disposable worker and ISO composer | Planned |
| `jfdelnero/LinuxFromScratch` | target profiles, patch framework, embedded outputs | provider/profile inheritance and target adapters | Schema direction implemented; providers planned |

## Why blanket 100% parity is not used

- Some reference behavior is unsafe or hard-coded and should be replaced, not
  duplicated.
- One project is a desktop application suite rather than an LFS builder.
- One project covers embedded boards and architectures outside this project's
  initial i386/x86_64 scope.
- Reference heads and upstream books continue to move.
- GPL and unlicensed code cannot simply be folded into a 0BSD codebase.

Every relevant behavior will map to a test, an evidence claim, or a written
out-of-scope rationale.
