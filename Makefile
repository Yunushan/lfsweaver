.PHONY: test check examples plan

test:
	PYTHONPATH=src python3 -m unittest discover -s tests -v

check: test
	PYTHONPATH=src python3 -m lfsweaver evidence evidence/support.json
	PYTHONPATH=src python3 scripts/validate_examples.py

examples:
	PYTHONPATH=src python3 scripts/validate_examples.py

plan:
	PYTHONPATH=src python3 -m lfsweaver plan examples/lfs-13.0-systemd-x86_64.toml
