# Upstream lifecycle

The scheduled watcher reads official project news and refs. A newly observed
stable release is not automatically considered supported.

## Update flow

1. Detect a new stable, RC, development commit, advisory, or source checksum
   change.
2. Create a lock-update branch with book commits/tags, source URLs and SHA-256,
   patches and SHA-256, and the worker image digest.
3. Produce a semantic diff of package versions, build commands, dependencies,
   XML structures, kernel/boot configuration, and removals.
4. Stop when unknown XML or command structures are encountered.
5. Run isolated canary builds.
6. Run the full stable matrix twice after review.
7. Publish new evidence only for the combinations that pass every gate.

Failures update one tracking issue with the phase, normalized error, affected
claim IDs, and report links. They do not silently fall back to an older package
or weaken tests.

The release watcher is therefore autonomous at detection and triage. It is not
a promise that arbitrary future book changes can be safely understood without
human judgment.
