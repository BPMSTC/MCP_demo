"""Repository analysis utilities for the MCP onboarding demo.

The functions in this module are intentionally lightweight and read-only.
They avoid executing user code, shelling out to external tooling, or mutating
the repository. This keeps the demo safe while still producing useful context.
"""

from pathlib import Path

# Maximum number of characters to read from each file during summarization.
# This cap keeps responses compact and prevents accidental large payloads.
MAX_SUMMARY_READ_CHARS = 12_000

# Number of non-empty preview lines to include for each summarized file.
MAX_PREVIEW_LINES = 8

# Common directories that are not useful for source-entry analysis.
IGNORED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "mcpdemo",
    "site-packages",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
}


def _is_virtualenv_subpath(path: Path, root: Path, cache: dict[Path, bool]) -> bool:
    """Return True when `path` is under a directory containing pyvenv.cfg.

    The cache keeps repeated ancestor checks cheap during recursive scans.
    """
    try:
        relative_parts = path.relative_to(root).parts
    except ValueError:
        return False

    for idx in range(1, len(relative_parts)):
        candidate = root.joinpath(*relative_parts[:idx])
        if candidate not in cache:
            cache[candidate] = (candidate / "pyvenv.cfg").exists()
        if cache[candidate]:
            return True

    return False

# Filename-based heuristics and their relative confidence weights.
ENTRY_POINT_SCORES = {
    "main.py": 100,
    "app.py": 90,
    "server.py": 90,
    "manage.py": 85,
    "index.js": 85,
    "index.ts": 85,
    "program.cs": 95,
    "package.json": 70,
    "pyproject.toml": 65,
    "requirements.txt": 60,
    "dockerfile": 70,
    "docker-compose.yml": 70,
    "docker-compose.yaml": 70,
    "readme.md": 55,
}


def _safe_read_text(path: Path, max_chars: int = MAX_SUMMARY_READ_CHARS) -> str:
    """Read text from a file safely and return up to `max_chars` characters.

    UTF-8 is attempted first because it is the most common encoding for source
    files. If decoding fails, we fall back to replacement mode so the call can
    still return a useful best-effort summary instead of raising.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")
    return text[:max_chars]


def _looks_binary(path: Path) -> bool:
    """Quickly detect likely binary files.

    The function checks the first chunk for a null byte, which is a common
    binary indicator. This is intentionally simple and fast for demo purposes.
    """
    try:
        chunk = path.read_bytes()[:1024]
    except OSError:
        return False
    return b"\x00" in chunk


def _file_purpose_hint(path: Path, content: str) -> str:
    """Infer a coarse-grained purpose hint based on file name and content."""
    name = path.name.lower()
    lowered = content.lower()

    if name in {"readme.md", "readme.txt"}:
        return "Repository overview and setup guidance."
    if name in {"requirements.txt", "pyproject.toml", "package.json"}:
        return "Dependency and project configuration metadata."
    if name in {"dockerfile", "docker-compose.yml", "docker-compose.yaml"}:
        return "Container build/runtime configuration."
    if "@mcp.tool" in content or "fastmcp" in lowered:
        return "MCP server surface area and tool registration logic."
    if "if __name__ == \"__main__\"" in content:
        return "Likely executable entry script."
    if "def main(" in content or "class" in content:
        return "Application logic and callable code units."
    return "General repository file."


def summarize_files(paths: list[str]) -> str:
    """Summarize one or more repository files.

    Parameters
    ----------
    paths:
        Relative or absolute file paths supplied by an MCP client.

    Returns
    -------
    str
        Markdown-formatted summary with metadata, purpose hints, and previews.

    Notes
    -----
    - The function is read-only and never executes file contents.
    - Missing files are reported inline so callers can self-correct quickly.
    - Binary files are identified and skipped to avoid noisy output.
    """
    if not paths:
        return "No file paths were provided. Pass one or more paths to summarize."

    summaries: list[str] = ["# File Summaries"]
    cwd = Path.cwd()

    for raw_path in paths:
        requested = Path(raw_path)
        resolved = requested if requested.is_absolute() else (cwd / requested)
        resolved = resolved.resolve()

        summaries.append(f"\n## {raw_path}")

        if not resolved.exists():
            summaries.append(f"- Status: Missing path ({resolved})")
            continue

        if resolved.is_dir():
            child_count = sum(1 for _ in resolved.iterdir())
            summaries.append("- Type: Directory")
            summaries.append(f"- Resolved path: {resolved}")
            summaries.append(f"- Direct children: {child_count}")
            summaries.append("- Note: summarize_files expects file paths for deep summaries.")
            continue

        if _looks_binary(resolved):
            summaries.append("- Type: Binary file")
            summaries.append("- Note: Binary content skipped to keep output readable.")
            continue

        try:
            content = _safe_read_text(resolved)
        except OSError as exc:
            summaries.append(f"- Status: Could not read file ({exc})")
            continue

        line_count = content.count("\n") + (1 if content else 0)
        purpose = _file_purpose_hint(resolved, content)

        non_empty_lines = [line.rstrip() for line in content.splitlines() if line.strip()]
        preview_lines = non_empty_lines[:MAX_PREVIEW_LINES]

        summaries.append("- Type: File")
        summaries.append(f"- Resolved path: {resolved}")
        summaries.append(f"- Extension: {resolved.suffix or '(none)'}")
        summaries.append(f"- Characters analyzed: {len(content)}")
        summaries.append(f"- Lines analyzed: {line_count}")
        summaries.append(f"- Purpose hint: {purpose}")

        if preview_lines:
            summaries.append("- Preview:")
            summaries.append("```text")
            summaries.extend(preview_lines)
            summaries.append("```")
        else:
            summaries.append("- Preview: File appears empty in analyzed range.")

    return "\n".join(summaries)


def find_entry_points(root_path: str = ".") -> str:
    """Identify likely repository entry points and startup-related files.

    The scoring model combines filename heuristics with lightweight content
    signals (for example, Python main guards). The output is intentionally
    human-readable markdown so it can be pasted directly into onboarding notes.
    """
    root = Path(root_path).resolve()
    if not root.exists():
        return f"Root path does not exist: {root}"
    if not root.is_dir():
        return f"Root path is not a directory: {root}"

    candidates: list[tuple[int, Path, list[str]]] = []
    venv_path_cache: dict[Path, bool] = {}

    for path in root.rglob("*"):
        if path.is_dir():
            continue

        # Skip generated and dependency-heavy paths early for speed/readability.
        if any(part.lower() in IGNORED_DIRS for part in path.parts):
            continue
        if _is_virtualenv_subpath(path, root, venv_path_cache):
            continue

        name = path.name.lower()
        score = ENTRY_POINT_SCORES.get(name, 0)
        reasons: list[str] = []

        if score:
            reasons.append(f"recognized filename heuristic ({name})")

        # Apply low-cost content checks only for likely code/config file types.
        if path.suffix.lower() in {".py", ".js", ".ts", ".md", ".toml", ".yml", ".yaml", ".json", ""}:
            try:
                content = _safe_read_text(path, max_chars=6_000)
            except OSError:
                content = ""

            lowered = content.lower()
            if "if __name__ == \"__main__\"" in content:
                score += 40
                reasons.append("contains Python main guard")
            if "def main(" in content:
                score += 20
                reasons.append("contains main() definition")
            if "fastmcp" in lowered or "@mcp.tool" in lowered:
                score += 25
                reasons.append("contains MCP server/tool signal")
            if "uvicorn" in lowered or "flask" in lowered or "fastapi" in lowered:
                score += 15
                reasons.append("contains web app startup dependency")

        if score > 0:
            candidates.append((score, path, reasons))

    if not candidates:
        return (
            "No likely entry points were identified with current heuristics. "
            "Try pointing to a different root path or adding additional patterns."
        )

    candidates.sort(key=lambda item: item[0], reverse=True)
    top_candidates = candidates[:12]

    lines: list[str] = [
        "# Likely Entry Points",
        f"Scanned root: {root}",
        f"Candidates found: {len(candidates)}",
        "",
        "## Top Results",
    ]

    for score, path, reasons in top_candidates:
        rel_path = path.relative_to(root)
        lines.append(f"- {rel_path} (score: {score})")
        if reasons:
            lines.append(f"  Reasons: {', '.join(reasons)}")

    lines.append("\n## Suggested Reading Order")
    lines.append("1. Highest-scoring executable or server file.")
    lines.append("2. Dependency/config files (for runtime assumptions).")
    lines.append("3. README and architecture docs for workflow context.")

    return "\n".join(lines)
