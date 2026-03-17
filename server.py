"""Repo Onboarding Assistant MCP server.

This module wires together MCP primitives (tools, resources, prompts) so an
AI client can onboard quickly in an unfamiliar codebase. Handlers are designed
to be deterministic, read-only, and easy to inspect during demos.
"""

from pathlib import Path

from fastmcp import FastMCP

from repo_tools import find_entry_points, summarize_files

mcp = FastMCP("repo-onboarding-assistant")


def _read_text_or_fallback(path: Path, fallback: str) -> str:
    """Read UTF-8 text from `path`, returning `fallback` on any failure.

    We intentionally return fallback text instead of raising so MCP clients get
    informative responses even when optional documentation files are missing.
    """
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return fallback


@mcp.tool()
def summarize_files_tool(paths: list[str]) -> str:
    """Return a concise summary for one or more files.

    This MCP tool delegates to `repo_tools.summarize_files`, which performs
    bounded, read-only analysis and returns markdown suitable for chat output.
    """
    return summarize_files(paths)


@mcp.tool()
def find_entry_points_tool(root_path: str = ".") -> str:
    """Identify likely repository entry points.

    The tool surfaces startup-related files and ranks them by confidence so a
    developer can decide where to begin reading code.
    """
    return find_entry_points(root_path)


@mcp.resource("project://architecture")
def architecture_resource() -> str:
    """Return the architecture resource content.

    MCP resources should return actual payload content. For this demo, the
    payload is a markdown document under resources/architecture.md.
    """
    architecture_path = Path(__file__).parent / "resources" / "architecture.md"
    return _read_text_or_fallback(
        architecture_path,
        "Architecture resource is unavailable. Expected file: resources/architecture.md",
    )


@mcp.prompt()
def generate_onboarding_summary(project_name: str = "this project") -> str:
    """Generate a reusable onboarding brief.

    The prompt combines a static onboarding template, live entry-point hints,
    and architecture context so an MCP client can produce a high-quality,
    repository-specific onboarding document.
    """
    root = Path(__file__).parent
    template_path = root / "prompts" / "onboarding_prompt.txt"
    architecture_path = root / "resources" / "architecture.md"

    template = _read_text_or_fallback(
        template_path,
        "Template missing: prompts/onboarding_prompt.txt",
    )
    architecture = _read_text_or_fallback(
        architecture_path,
        "Architecture context missing: resources/architecture.md",
    )
    entry_points = find_entry_points(str(root))

    return (
        f"# Onboarding Prompt For {project_name}\n\n"
        "Use the guidance below to generate an onboarding summary.\n\n"
        "## Template\n"
        f"{template}\n\n"
        "## Architecture Context\n"
        f"{architecture}\n\n"
        "## Likely Entry Points\n"
        f"{entry_points}\n"
    )


if __name__ == "__main__":
    mcp.run()
