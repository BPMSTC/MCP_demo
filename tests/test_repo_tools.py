"""Unit tests for repository analysis helpers.

These tests focus on observable behavior rather than implementation details,
which keeps them resilient if heuristics evolve over time.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from repo_tools import find_entry_points, summarize_files


class SummarizeFilesTests(unittest.TestCase):
    """Behavioral tests for summarize_files."""

    def test_returns_helpful_message_for_empty_input(self) -> None:
        """The function should guide callers when no paths are provided."""
        output = summarize_files([])
        self.assertIn("No file paths were provided", output)

    def test_summarizes_text_file_with_metadata(self) -> None:
        """A normal text file should include core summary signals."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            target = root / "main.py"
            target.write_text(
                "def main():\n"
                "    return 'ok'\n\n"
                "if __name__ == \"__main__\":\n"
                "    print(main())\n",
                encoding="utf-8",
            )

            output = summarize_files([str(target)])

            self.assertIn("# File Summaries", output)
            self.assertIn("Type: File", output)
            self.assertIn("Purpose hint", output)
            self.assertIn("def main():", output)

    def test_reports_missing_file(self) -> None:
        """Missing files should be reported clearly and not raise exceptions."""
        output = summarize_files(["does-not-exist.txt"])
        self.assertIn("Status: Missing path", output)


class FindEntryPointsTests(unittest.TestCase):
    """Behavioral tests for find_entry_points."""

    def test_returns_error_for_missing_root(self) -> None:
        """A missing scan root should return a clear error message."""
        output = find_entry_points("path-that-does-not-exist")
        self.assertIn("Root path does not exist", output)

    def test_ranks_likely_entry_files(self) -> None:
        """main.py should be detected as a likely startup candidate."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            main = root / "main.py"
            readme = root / "README.md"

            main.write_text(
                "def main():\n"
                "    print('hello')\n\n"
                "if __name__ == \"__main__\":\n"
                "    main()\n",
                encoding="utf-8",
            )
            readme.write_text("# Demo\n", encoding="utf-8")

            output = find_entry_points(str(root))

            self.assertIn("# Likely Entry Points", output)
            self.assertIn("main.py", output)
            self.assertIn("Suggested Reading Order", output)


if __name__ == "__main__":
    unittest.main()
