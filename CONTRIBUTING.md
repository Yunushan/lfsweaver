# Contributing

Thank you for helping make LFS builds safer and more reproducible.

## Before opening a pull request

1. Keep original contributions compatible with the repository's 0BSD license.
2. Do not paste code from GPL or unlicensed reference projects.
3. Preserve all applicable upstream notices for fetched or generated content.
4. Add or update tests for every behavior change.
5. Never promote a support claim without the evidence required by
   `docs/verification.md`.
6. Keep destructive operations inside the disposable Linux worker and default
   them to dry-run behavior.

Run locally:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m lfsweaver evidence evidence/support.json
for manifest in examples/*.toml; do
  PYTHONPATH=src python3 -m lfsweaver validate "$manifest"
done
```

Provider changes should include a pinned upstream fixture, semantic-diff
snapshot, source checksums, license metadata, and a fail-closed test for unknown
input.
