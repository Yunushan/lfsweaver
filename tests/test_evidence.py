from __future__ import annotations

import unittest

from lfsweaver.evidence import validate_evidence


class EvidenceTests(unittest.TestCase):
    def test_planned_claim_needs_no_proof(self) -> None:
        data = {"schema_version": 1, "claims": [{"id": "future", "state": "planned"}]}
        self.assertEqual(validate_evidence(data), [])

    def test_verified_claim_without_proof_fails(self) -> None:
        data = {"schema_version": 1, "claims": [{"id": "claim", "state": "verified"}]}
        self.assertIn("proof is required", "; ".join(validate_evidence(data)))

    def test_tested_claim_without_proof_fails(self) -> None:
        data = {"schema_version": 1, "claims": [{"id": "claim", "state": "tested"}]}
        self.assertIn("proof is required", "; ".join(validate_evidence(data)))

    def test_verified_claim_with_proof_passes(self) -> None:
        data = {
            "schema_version": 1,
            "claims": [
                {
                    "id": "claim",
                    "state": "verified",
                    "proof": {
                        "workflow_url": "https://github.com/example/actions/runs/1",
                        "report_url": "https://example.test/report.json",
                        "verified_at": "2026-07-15T00:00:00Z",
                        "artifact_sha256": "a" * 64,
                    },
                }
            ],
        }
        self.assertEqual(validate_evidence(data), [])


if __name__ == "__main__":
    unittest.main()
