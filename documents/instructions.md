from pathlib import Path

content = """# Repo Onboarding Assistant MCP Server

## Project Summary

This project is a lightweight **Model Context Protocol (MCP) server** designed for a developer audience. Its purpose is to help an AI client act like a useful repo onboarding assistant by exposing carefully selected repository context and developer-oriented helper actions through MCP.

The demo is intentionally small, practical, and easy to explain live. Instead of using an academic or classroom example, it focuses on a problem most developers recognize immediately: **understanding an unfamiliar codebase quickly and safely**.

## Core Idea

The server gives an AI client controlled access to three kinds of MCP capabilities:

- **Tools** for active operations
- **Resources** for structured reference material
- **Prompts** for repeatable developer workflows

This makes the project a clean demonstration of how MCP standardizes client-server interaction while still solving a real engineering problem.

## Demo Goal

Show how an MCP server can help a developer:

- understand a repository faster
- identify likely entry points
- summarize architecture and setup information
- generate onboarding or handoff content
- answer basic repo questions without exposing the entire environment recklessly

## Recommended Demo Framing

**Pitch:**
“Here is a small MCP server that helps an AI client onboard a developer into a repository. It exposes a few safe repo-aware capabilities so the client can inspect context, summarize code structure, and generate useful onboarding outputs.”

That framing works because it is concrete, practical, and not soaked in tutorial weather data for the thousandth time.

## Proposed Capabilities

### 1. Tool: `summarize_files`

Accepts one or more file paths and returns a concise technical summary.

**Use cases**

- summarize `README.md`
- summarize `package.json`
- summarize a controller or service file
- explain the role of a config file

**Why it matters**
This shows an action-oriented MCP capability that the AI client can invoke when needed.

### 2. Tool: `find_entry_points`

Scans a repo or selected folder and identifies likely starting points such as:

- main application entry file
- API bootstrap file
- dependency injection configuration
- routing definitions
- build and deployment files

**Why it matters**
Developers immediately understand the value of this. It also makes for a strong live demo.

### 3. Resource: `project://architecture`

Returns a curated architecture summary for the repository.

**Example contents**

- project purpose
- major folders
- key runtime components
- important dependencies
- common workflow notes

**Why it matters**
This demonstrates that resources can provide stable, retrievable context instead of just triggering actions.

### 4. Prompt: `generate_onboarding_summary`

Produces a reusable onboarding brief for a new developer.

**Possible output**

- what this project does
- where to start reading
- what to run first
- common pain points
- first debugging checkpoints

**Why it matters**
This is a good example of how prompts differ from tools and resources. It also feels highly relevant to real engineering teams.

## Technical Stack

- **Python**
- **FastMCP**
- local repo access through standard file operations
- optional MCP Inspector for testing
- optional Claude Desktop or another MCP-compatible client for live invocation
