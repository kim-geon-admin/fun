from __future__ import annotations

import unittest

from cddex.classifier import classify


class ClassifierTests(unittest.TestCase):
    def test_korean_error_and_file_request_returns_ordered_intents(self) -> None:
        self.assertEqual(
            classify("README 파일에서 로그인 오류를 찾아줘"),
            ("file", "search", "error"),
        )

    def test_unmatched_request_is_general(self) -> None:
        self.assertEqual(classify("오늘 재미있는 생각을 해보자"), ("general",))


if __name__ == "__main__":
    unittest.main()

