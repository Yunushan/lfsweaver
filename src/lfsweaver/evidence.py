"""Validation for support claims and build evidence."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .constants import EVIDENCE_STATES

_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class EvidenceError(ValueError):
    pass


def validate_evidence(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    claims = data.get("claims")
    if not isinstance(claims, list):
        return errors + ["claims must be an array"]

    seen: set[str] = set()
    for index, claim in enumerate(claims):
        prefix = f"claims[{index}]"
        if not isinstance(claim, dict):
            errors.append(f"{prefix} must be an object")
            continue
        claim_id = claim.get("id")
        if not isinstance(claim_id, str) or not claim_id:
            errors.append(f"{prefix}.id must be a non-empty string")
        elif claim_id in seen:
            errors.append(f"duplicate claim id: {claim_id}")
        else:
            seen.add(claim_id)
        state = claim.get("state")
        if state not in EVIDENCE_STATES:
            errors.append(f"{prefix}.state must be one of {', '.join(EVIDENCE_STATES)}")
            continue
        if state in {"tested", "verified"}:
            proof = claim.get("proof")
            if not isinstance(proof, dict):
                errors.append(f"{prefix}.proof is required for {state} claims")
                continue
            required = ["workflow_url", "report_url", "verified_at"]
            if state == "verified":
                required.append("artifact_sha256")
            for field in required:
                if not isinstance(proof.get(field), str) or not proof[field]:
                    errors.append(f"{prefix}.proof.{field} is required")
            digest = proof.get("artifact_sha256", "")
            if isinstance(digest, str) and digest and not _SHA256.fullmatch(digest):
                errors.append(f"{prefix}.proof.artifact_sha256 must be 64 lowercase hex characters")
            for field in ("workflow_url", "report_url"):
                url = proof.get(field, "")
                if isinstance(url, str) and url and not url.startswith("https://"):
                    errors.append(f"{prefix}.proof.{field} must use HTTPS")
    return errors


def load_evidence(path: str | Path) -> dict[str, Any]:
    evidence_path = Path(path)
    try:
        data = json.loads(evidence_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise EvidenceError(f"evidence file not found: {evidence_path}") from exc
    except json.JSONDecodeError as exc:
        raise EvidenceError(f"invalid JSON in {evidence_path}: {exc}") from exc
    if not isinstance(data, dict):
        raise EvidenceError("evidence root must be an object")
    errors = validate_evidence(data)
    if errors:
        raise EvidenceError("; ".join(errors))
    return data
