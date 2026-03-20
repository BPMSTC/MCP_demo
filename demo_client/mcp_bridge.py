"""MCP client bridge for the guided browser demo app.

This module provides a small synchronous facade over the FastMCP async client
APIs so Streamlit button handlers can invoke MCP operations directly.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

from fastmcp import Client
from fastmcp.client.transports.stdio import StdioTransport


def _to_pretty_json(value: Any) -> str:
    """Render a model-like object to pretty JSON when possible."""
    if hasattr(value, "model_dump_json"):
        return value.model_dump_json(indent=2)
    return str(value)


def _resource_to_text(resource_item: Any) -> str:
    """Normalize resource content blocks to display text."""
    if hasattr(resource_item, "text") and resource_item.text is not None:
        return str(resource_item.text)
    if hasattr(resource_item, "blob") and resource_item.blob is not None:
        return "[binary blob omitted]"
    return str(resource_item)


def _prompt_to_text(prompt_result: Any) -> str:
    """Normalize prompt responses to markdown-like text for display."""
    messages = getattr(prompt_result, "messages", []) or []
    chunks: list[str] = []

    for idx, message in enumerate(messages, start=1):
        role = getattr(message, "role", "unknown")
        content = getattr(message, "content", None)

        text = None
        if content is not None:
            text = getattr(content, "text", None)
            if text is None and hasattr(content, "model_dump_json"):
                text = content.model_dump_json(indent=2)

        if text is None:
            text = str(content)

        chunks.append(f"### Message {idx} ({role})\n{text}")

    if not chunks:
        return _to_pretty_json(prompt_result)

    return "\n\n".join(chunks)


class DemoMCPClient:
    """Synchronous wrapper around an MCP stdio client for demo interactions."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.python_exe = repo_root / "mcpdemo" / "Scripts" / "python.exe"
        self.server_script = repo_root / "server.py"

    def _build_transport(self) -> StdioTransport:
        return StdioTransport(
            command=str(self.python_exe),
            args=[str(self.server_script)],
            cwd=str(self.repo_root),
            keep_alive=False,
        )

    async def _list_capabilities_async(self) -> dict[str, list[str]]:
        transport = self._build_transport()
        client = Client(transport)
        async with client:
            tools = await client.list_tools()
            resources = await client.list_resources()
            prompts = await client.list_prompts()

        return {
            "tools": [tool.name for tool in tools],
            "resources": [str(resource.uri) for resource in resources],
            "prompts": [prompt.name for prompt in prompts],
        }

    async def _run_entry_points_async(self, root_path: str) -> str:
        transport = self._build_transport()
        client = Client(transport)
        async with client:
            result = await client.call_tool(
                "find_entry_points_tool", {"root_path": root_path}
            )

        data = result.data
        return data if isinstance(data, str) else _to_pretty_json(result)

    async def _run_summaries_async(self, paths: list[str]) -> str:
        transport = self._build_transport()
        client = Client(transport)
        async with client:
            result = await client.call_tool("summarize_files_tool", {"paths": paths})

        data = result.data
        return data if isinstance(data, str) else _to_pretty_json(result)

    async def _run_architecture_async(self) -> str:
        transport = self._build_transport()
        client = Client(transport)
        async with client:
            contents = await client.read_resource("project://architecture")

        if not contents:
            return "No resource payload returned."

        return "\n\n".join(_resource_to_text(item) for item in contents)

    async def _run_onboarding_prompt_async(self, project_name: str) -> str:
        transport = self._build_transport()
        client = Client(transport)
        async with client:
            result = await client.get_prompt(
                "generate_onboarding_summary", {"project_name": project_name}
            )

        return _prompt_to_text(result)

    def _run_sync(self, coro: Any) -> Any:
        return asyncio.run(coro)

    def list_capabilities(self) -> dict[str, list[str]]:
        return self._run_sync(self._list_capabilities_async())

    def run_entry_points(self, root_path: str) -> str:
        return self._run_sync(self._run_entry_points_async(root_path))

    def run_summaries(self, paths: list[str]) -> str:
        return self._run_sync(self._run_summaries_async(paths))

    def run_architecture(self) -> str:
        return self._run_sync(self._run_architecture_async())

    def run_onboarding_prompt(self, project_name: str) -> str:
        return self._run_sync(self._run_onboarding_prompt_async(project_name))
