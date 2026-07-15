# jhalfs compatibility adapter

The official ALFS implementation, jhalfs, extracts instructions from LFS book
XML and generates ordered build scripts. LFSWeaver will use it behind a
versioned provider boundary rather than vendoring or rewriting the book.

The adapter must:

- pin the jhalfs commit and book commit/tag;
- preserve applicable MIT and LFS notices on generated instructions;
- generate configuration noninteractively from a validated manifest;
- place all privileged work inside a disposable Linux worker;
- archive jhalfs logs and upstream test results;
- stop on unknown book structures or missing source checksums;
- never report BLFS-wide verification when only a curated package profile ran.

No jhalfs source is vendored in this directory today.
