from __future__ import annotations

import unittest

from lfsweaver.upstream import UpstreamError, parse_latest_release


class UpstreamTests(unittest.TestCase):
    def test_latest_release_is_semantic_not_lexical(self) -> None:
        body = "LFS-9.1 Release LFS-12.4 Release LFS-13.0 Release"
        self.assertEqual(parse_latest_release("lfs", body), "13.0")

    def test_rc_is_not_selected(self) -> None:
        body = "LFS-13.1-rc1 Release LFS-13.0 Release"
        self.assertEqual(parse_latest_release("lfs", body), "13.0")

    def test_blfs_news_wording_is_supported(self) -> None:
        body = "BLFS 12.4 has been released! BLFS 13.0 has been released!"
        self.assertEqual(parse_latest_release("blfs", body), "13.0")

    def test_missing_release_fails_closed(self) -> None:
        with self.assertRaises(UpstreamError):
            parse_latest_release("lfs", "redesigned page with no recognizable release")


if __name__ == "__main__":
    unittest.main()
