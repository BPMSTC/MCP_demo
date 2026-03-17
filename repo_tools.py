"""Scaffold utilities for repository analysis.

Implementations are intentionally minimal in this scaffold-only phase.
"""

from pathlib import Path


def summarize_files(paths: list[str]) -> str:
    """Placeholder: summarize a list of files."""
    resolved = [str(Path(p)) for p in paths]
    return (
        "Scaffold placeholder: summarize_files is not fully implemented yet. "
        f"Received paths: {resolved}"
    )


def find_entry_points(root_path: str = ".") -> str:
    """Placeholder: locate likely application entry points."""
    root = Path(root_path)
    return (
        "Scaffold placeholder: find_entry_points is not fully implemented yet. "
        f"Scan root: {root}"
    )
