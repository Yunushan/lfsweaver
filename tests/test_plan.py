from __future__ import annotations

import unittest

from lfsweaver.manifest import parse_manifest
from lfsweaver.plan import create_plan
from test_manifest import base_manifest


class PlanTests(unittest.TestCase):
    def test_plan_is_deterministic(self) -> None:
        manifest = parse_manifest(base_manifest())
        first = create_plan(manifest)
        second = create_plan(manifest)
        self.assertEqual(first.digest(), second.digest())
        self.assertEqual(first.as_dict(), second.as_dict())

    def test_iso_plan_contains_install_test(self) -> None:
        data = base_manifest()
        data["target"]["outputs"] = ["rootfs", "iso"]
        data["verification"].update({"boot": True, "install": True})
        plan = create_plan(parse_manifest(data))
        ids = [step.id for step in plan.steps]
        self.assertIn("compose-iso", ids)
        self.assertIn("boot-test", ids)
        self.assertIn("install-test", ids)

    def test_cluster_plan_has_e2e_gate(self) -> None:
        data = base_manifest()
        data["target"]["outputs"] = ["raw", "k3s"]
        data["verification"]["boot"] = True
        plan = create_plan(parse_manifest(data))
        self.assertIn("cluster-test", [step.id for step in plan.steps])


if __name__ == "__main__":
    unittest.main()
