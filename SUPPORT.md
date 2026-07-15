# Support

Use GitHub Discussions for design and usage questions and GitHub Issues for
reproducible defects or upstream compatibility failures.

Include:

- `lfsweaver --version`;
- controller OS and architecture;
- `lfsweaver doctor --json` output (review it for private hostnames first);
- sanitized manifest and plan digest;
- exact upstream version/commit;
- executor and worker image/hypervisor;
- failed step ID and report/log link.

Never post credentials, tokens, private SSH keys, proprietary package sources,
or complete environment dumps.

Only combinations marked `verified` in `evidence/support.json` are release
supported. Planned and experimental entries are welcome test targets but do not
carry compatibility guarantees.
