"""Scaffold for Repo Onboarding Assistant MCP server.

This file intentionally contains only structural placeholders.
"""

from fastmcp import FastMCP

from repo_tools import find_entry_points, summarize_files

mcp = FastMCP("repo-onboarding-assistant")


@mcp.tool()
def summarize_files_tool(paths: list[str]) -> str:
    """Return a concise summary for one or more files."""
    return summarize_files(paths)


@mcp.tool()
def find_entry_points_tool(root_path: str = ".") -> str:
    """Identify likely repository entry points."""
    return find_entry_points(root_path)


@mcp.resource("project://architecture")
def architecture_resource() -> str:
    """Return a curated architecture overview."""
    return "resources/architecture.md"


@mcp.prompt()
def generate_onboarding_summary(project_name: str = "this project") -> str:
    """Generate a reusable onboarding brief."""
    return (
        f"Use prompts/onboarding_prompt.txt as a template to create an onboarding summary for {project_name}."
    )


if __name__ == "__main__":
    mcp.run()
