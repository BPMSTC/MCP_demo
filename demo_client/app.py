"""Guided browser experience for the Repo Onboarding Assistant MCP demo."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from mcp_bridge import DemoMCPClient

REPO_ROOT = Path(__file__).resolve().parent.parent

st.set_page_config(
    page_title="MCP Guided Demo",
    page_icon="MCP",
    layout="wide",
)


def validate_repo_path(path_str: str) -> tuple[bool, str, Path | None]:
    """Validate and normalize a repository path."""
    if not path_str or not path_str.strip():
        return False, "Path cannot be empty.", None

    try:
        path = Path(path_str.strip()).resolve()
    except (ValueError, OSError) as exc:
        return False, f"Invalid path: {exc}", None

    if not path.exists():
        return False, f"Path does not exist: {path}", None

    if not path.is_dir():
        return False, f"Path is not a directory: {path}", None

    has_python = any(path.glob("**/*.py"))
    if not has_python:
        return (
            False,
            f"No Python files found in {path}. Point to a Python project directory.",
            None,
        )

    return True, "", path


def discover_local_repos(workspace_root: Path) -> list[Path]:
    """Return likely Python repositories for quick selection."""
    candidates: list[Path] = []

    for child in sorted(workspace_root.iterdir(), key=lambda p: p.name.lower()):
        if not child.is_dir():
            continue
        if child.name.startswith(".") or child.name in {"mcpdemo", "__pycache__", "tests"}:
            continue
        if any(child.glob("**/*.py")):
            candidates.append(child)

    # Always keep the current sample repo first for demos.
    sample = workspace_root / "sample_repo"
    if sample.exists() and sample not in candidates:
        candidates.insert(0, sample)
    elif sample in candidates:
        candidates.remove(sample)
        candidates.insert(0, sample)

    return candidates


st.title("Repo Onboarding Assistant: Guided MCP Demo")
st.markdown(
    "A professional interface for exploring Python repository structure through MCP over stdio transport."
)

SUMMARY_DEFAULTS: dict[str, str] = {
    "sample_repo": "README.md\nsrc/main.py\nconfig/app.yaml",
    "sample_repo_service": (
        "README.md\npyproject.toml\nservice/app.py\nworkers/scheduler.py\nconfig/settings.py"
    ),
}

with st.sidebar:
    st.header("Target Repository")
    st.markdown(
        "Set **Repository path** to the Python project you want to analyze. "
        "This can be inside this workspace or any other local repository."
    )

    local_repo_options = discover_local_repos(REPO_ROOT)
    option_map = {f"{repo.name} - {repo}": str(repo) for repo in local_repo_options}

    selected_repo_label = st.selectbox(
        "Quick-select repository",
        options=list(option_map.keys()) if option_map else ["No local repo options found"],
        help=(
            "Pick from detected local Python repositories so you can switch targets "
            "without typing a full path."
        ),
    )

    selected_repo_path = option_map.get(selected_repo_label)
    selected_repo_name = Path(selected_repo_path).name if selected_repo_path else None

    if "last_selected_repo" not in st.session_state:
        st.session_state.last_selected_repo = selected_repo_name

    # Auto-fill sidebar defaults when quick-select repository changes.
    if selected_repo_name and st.session_state.last_selected_repo != selected_repo_name:
        st.session_state.target_repo_input = selected_repo_path
        st.session_state.summary_paths = SUMMARY_DEFAULTS.get(
            selected_repo_name,
            "README.md\nrequirements.txt",
        )
        st.session_state.root_path = "."
        st.session_state.project_name = selected_repo_name
        st.session_state.last_selected_repo = selected_repo_name

    with st.expander("Example paths", expanded=True):
        st.markdown(f"- {REPO_ROOT / 'sample_repo'}")
        st.markdown(f"- {REPO_ROOT / 'sample_repo_service'}")
        st.markdown("- C:/repos/my_project")
        st.markdown("- ../another_project")

    target_repo_input = st.text_input(
        "Repository path",
        value=selected_repo_path or str(REPO_ROOT / "sample_repo"),
        key="target_repo_input",
        help=(
            "Path to a Python project directory. Pick one above or paste a custom path. "
            "This field is validated before actions are enabled."
        ),
    )

    is_valid, validation_msg, target_repo = validate_repo_path(target_repo_input)

    if is_valid:
        st.success("Valid repository")
    else:
        st.error(validation_msg)
        target_repo = None

    st.divider()
    st.subheader("Scan Settings")

    root_path = st.text_input(
        "Entry-point scan root",
        value=".",
        key="root_path",
        help=(
            "Subfolder inside Repository path where Step 1 scans for startup files "
            "such as main.py and __main__.py. Use . to scan the entire repository."
        ),
        disabled=target_repo is None,
    )

    summary_paths = st.text_area(
        "Files to summarize",
        value=SUMMARY_DEFAULTS.get(selected_repo_name or "", "README.md\nrequirements.txt"),
        height=90,
        key="summary_paths",
        help=(
            "Repository-relative file paths for Step 2, one per line. "
            "Each listed file is sent to summarize_files_tool."
        ),
        disabled=target_repo is None,
    )

    project_name = st.text_input(
        "Prompt project name",
        value=target_repo.name if target_repo else "",
        key="project_name",
        help=(
            "Project name sent to Step 4 (generate_onboarding_summary). "
            "It personalizes the onboarding output."
        ),
        disabled=target_repo is None,
    )

if "history" not in st.session_state:
    st.session_state.history = []

if not target_repo:
    st.warning(
        "Set a valid Repository path in the sidebar to enable MCP actions. "
        "The directory must contain Python files."
    )
    st.stop()

client = DemoMCPClient(REPO_ROOT)

st.markdown("---")
st.subheader("Connectivity and Capabilities (Step 0)")
st.info("Run this first to confirm MCP connectivity and list server surface area.")

if st.button("Connect and List Capabilities", type="primary", key="step0"):
    with st.spinner("Connecting to MCP server and listing capabilities..."):
        try:
            capabilities = client.list_capabilities()
            st.success("Connected successfully.")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**Tools**")
                st.write(capabilities["tools"])
            with col2:
                st.markdown("**Resources**")
                st.write(capabilities["resources"])
            with col3:
                st.markdown("**Prompts**")
                st.write(capabilities["prompts"])
        except Exception as exc:
            st.error(f"Connection failed: {exc}")

st.markdown("---")
st.subheader("Guided Exploration (Steps 1-4)")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("### Step 1: Find Entry Points")
    if st.button(
        "Run Find Entry Points",
        key="step1",
        help=(
            "Scans the selected Repository path within Entry-point scan root, then calls "
            "find_entry_points_tool to locate likely startup files."
        ),
    ):
        with st.spinner("Calling find_entry_points_tool..."):
            try:
                requested_root = Path(root_path.strip() or ".")
                scan_root = (
                    requested_root
                    if requested_root.is_absolute()
                    else (target_repo / requested_root).resolve()
                )
                output = client.run_entry_points(root_path=str(scan_root))
                st.session_state.history.append((
                    "Step 1: Find Entry Points",
                    "Tool call to find_entry_points_tool.",
                    output,
                ))
                st.success("Entry points discovered.")
            except Exception as exc:
                st.error(f"Tool call failed: {exc}")

    st.divider()

    st.markdown("### Step 3: Load Architecture Resource")
    if st.button(
        "Run Load Architecture",
        key="step3",
        help=(
            "Reads the project://architecture MCP resource for stable architecture context. "
            "This step does not use Files to summarize."
        ),
    ):
        with st.spinner("Reading project://architecture..."):
            try:
                output = client.run_architecture()
                st.session_state.history.append((
                    "Step 3: Load Architecture Resource",
                    "Resource read from project://architecture.",
                    output,
                ))
                st.success("Architecture loaded.")
            except Exception as exc:
                st.error(f"Resource read failed: {exc}")

with col_b:
    st.markdown("### Step 2: Summarize Core Files")
    st.caption("Summarize selected files for fast context.")
    if st.button(
        "Run Summarize Files",
        key="step2",
        help=(
            "Uses Files to summarize (one repository-relative path per line), then calls "
            "summarize_files_tool to produce concise summaries."
        ),
    ):
        with st.spinner("Calling summarize_files_tool..."):
            try:
                raw_paths = [line.strip() for line in summary_paths.splitlines() if line.strip()]
                paths: list[str] = []
                for raw in raw_paths:
                    maybe = Path(raw)
                    resolved = maybe if maybe.is_absolute() else (target_repo / maybe).resolve()
                    paths.append(str(resolved))
                if not paths:
                    st.warning("Add at least one file path in Files to summarize.")
                else:
                    output = client.run_summaries(paths=paths)
                    st.session_state.history.append((
                        "Step 2: Summarize Core Files",
                        "Tool call to summarize_files_tool.",
                        output,
                    ))
                    st.success("Summaries generated.")
            except Exception as exc:
                st.error(f"Tool call failed: {exc}")

    st.divider()

    st.markdown("### Step 4: Generate Onboarding Prompt")
    if st.button(
        "Run Generate Onboarding Prompt",
        key="step4",
        help=(
            "Uses Prompt project name and calls generate_onboarding_summary to produce "
            "structured onboarding guidance for the selected repository."
        ),
    ):
        with st.spinner("Calling generate_onboarding_summary..."):
            try:
                output = client.run_onboarding_prompt(project_name=project_name)
                st.session_state.history.append((
                    "Step 4: Generate Onboarding Prompt",
                    "Prompt retrieval from generate_onboarding_summary.",
                    output,
                ))
                st.success("Onboarding prompt generated.")
            except Exception as exc:
                st.error(f"Prompt call failed: {exc}")

st.markdown("---")
st.subheader("Results")
if not st.session_state.history:
    st.info("No steps run yet. Start with Step 0.")
else:
    st.markdown(f"Recorded results: {len(st.session_state.history)}")
    for idx, (title, explanation, output) in enumerate(reversed(st.session_state.history), start=1):
        with st.expander(title, expanded=(idx == 1)):
            st.caption(explanation)
            st.markdown(output)
