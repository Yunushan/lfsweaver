# Third-party notices

LFSWeaver does not currently vendor the Linux From Scratch books, jhalfs, the
six reference repositories, package source archives, or third-party patches.

Build providers will fetch pinned upstream content and retain its original
license and attribution. The following projects inform the design but their
code is not copied into the 0BSD controller:

- Linux From Scratch and its BLFS, ALFS, MLFS, GLFS, SLFS, Hints, and Patches
  projects;
- `eliaz5536/LFSInstaller` (MIT);
- `reinterpretcat/lfs` (MIT);
- `KeithDHedger/LFSDesktopProject` (GPL-3.0-or-later source notices);
- `lumenthi/Linux-From-Scratch`, `luisgbm/lfs-scripts`, and
  `jfdelnero/LinuxFromScratch` (no reusable root license identified during the
  audit; treated as all-rights-reserved).

When jhalfs integration lands, its applicable MIT notice and the applicable LFS
instruction notice will be included with generated scripts.
