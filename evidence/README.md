# Evidence ledger

`support.json` is the machine-readable source of truth for capability claims.
Documentation and release jobs must not promote a claim to `verified` unless
the exact released artifact has all of the following:

- a public, release-blocking workflow URL;
- a downloadable machine-readable test report;
- an artifact SHA-256 digest;
- a verification timestamp and named runner/hypervisor;
- the required boot, install, runtime, or cluster tests for that artifact type.

The states are `verified`, `tested`, `experimental`, `planned`, and
`unsupported`. A green badge in documentation must be generated from this
ledger; prose alone is not proof.
