"""Unit tests for server-level MCP handler functions.

These tests verify that the public handler functions return meaningful output
and include expected sections from their composed sources.
"""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

FAST_MCP_AVAILABLE = importlib.util.find_spec("fastmcp") is not None

if FAST_MCP_AVAILABLE:
    from server import (
        architecture_resource,
        find_entry_points_tool,
        generate_onboarding_summary,
        summarize_files_tool,
    )


class ServerHandlerTests(unittest.TestCase):
    """Tests for server.py tool/resource/prompt handlers."""

    @unittest.skipUnless(FAST_MCP_AVAILABLE, "fastmcp is not installed in current environment")
    def test_architecture_resource_returns_markdown_content(self) -> None:
        """Architecture resource should return loaded markdown, not a file path."""
        output = architecture_resource()
        self.assertIn("# Architecture Overview", output)
        self.assertIn("Project Purpose", output)

    @unittest.skipUnless(FAST_MCP_AVAILABLE, "fastmcp is not installed in current environment")
    def test_generate_onboarding_summary_includes_expected_sections(self) -> None:
        """Prompt output should include template, architecture, and entry sections."""
        output = generate_onboarding_summary("Demo Project")
        self.assertIn("# Onboarding Prompt For Demo Project", output)
        self.assertIn("## Template", output)
        self.assertIn("## Architecture Context", output)
        self.assertIn("## Likely Entry Points", output)

    @unittest.skipUnless(FAST_MCP_AVAILABLE, "fastmcp is not installed in current environment")
    def test_summarize_files_tool_with_single_temp_file(self) -> None:
        """Tool wrapper should delegate and return summary output for file input."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "notes.txt"
            path.write_text("hello\nworld\n", encoding="utf-8")

            output = summarize_files_tool([str(path)])

            self.assertIn("# File Summaries", output)
            self.assertIn("notes.txt", output)
            self.assertIn("Type: File", output)

    @unittest.skipUnless(FAST_MCP_AVAILABLE, "fastmcp is not installed in current environment")
    def test_find_entry_points_tool_returns_ranked_header(self) -> None:
        """Tool wrapper should return a structured ranking response."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "main.py"
            path.write_text(
                "def main():\n"
                "    pass\n\n"
                "if __name__ == \"__main__\":\n"
                "    main()\n",
                encoding="utf-8",
            )

            output = find_entry_points_tool(tmp_dir)

            self.assertIn("# Likely Entry Points", output)
            self.assertIn("main.py", output)


if __name__ == "__main__":
    unittest.main()
