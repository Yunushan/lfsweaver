# Support matrix policy

The canonical support state is `evidence/support.json`. Tables in documentation
are views of that ledger and must not be independently edited to show a higher
state.

Each artifact claim is keyed by at least:

```text
book family + upstream version/commit + init + architecture + profile + output
```

Controller claims additionally name the client OS and backend. Evidence always
records the project commit, workflow run, runner image/hardware, hypervisor or
runtime, artifact SHA-256, tests, and verification timestamp.

## State transitions

```text
planned -> experimental -> tested -> verified
                  \----------------> unsupported
```

Promotion is monotonic only for an exact immutable tuple. A new upstream book,
provider commit, worker image, kernel configuration, or artifact hash creates a
new tuple and must earn evidence again.

## Special constraints

- OCI images use the runtime host kernel and normally have no boot init; they
  must not be counted as proof of a bootable systemd/SysV disk.
- ISO verification includes installing to a blank disk and booting without the
  ISO attached.
- Raw images require firmware-specific boot tests.
- K3s/RKE2 claims refer to bootable node OS images and require cluster tests.
- GLFS GPU support requires named real hardware and driver combinations.
- Physical-install claims name the exact machine or hardware class tested.
