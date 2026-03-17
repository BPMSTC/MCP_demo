# Architecture Overview

## Project Purpose

Repo Onboarding Assistant is a lightweight MCP server that helps an AI client
understand a repository quickly and safely. The server focuses on read-only
operations that are useful during developer onboarding.

## Major Folders

- server.py
	- MCP server bootstrap and handler registration
- repo_tools.py
	- Core repository analysis logic used by MCP tools
- resources/
	- Stable markdown resources exposed through MCP resource URIs
- prompts/
	- Prompt templates used to generate repeatable onboarding workflows
- sample_repo/
	- Small sample codebase used for demo and testing scenarios
- tests/
	- Unit tests for tool behavior and output expectations

## Runtime Components

### FastMCP Server

- Instantiated in server.py as repo-onboarding-assistant
- Registers tools, resources, and prompts via decorators
- Runs as a local process using python server.py

### Repository Analysis Utilities

repo_tools.py provides two primary operations:

1. summarize_files(paths)
	 - Reads one or more files with bounded content size
	 - Skips binary files
	 - Returns markdown summaries with purpose hints and previews

2. find_entry_points(root_path)
	 - Recursively scans a repository
	 - Applies filename and content heuristics
	 - Returns ranked candidates and rationale for each item

### Prompt Composition Layer

generate_onboarding_summary composes:

- template guidance from prompts/onboarding_prompt.txt
- architecture context from this file
- live entry-point analysis from find_entry_points

This creates a reusable, context-rich prompt for AI-generated onboarding docs.

## Dependencies

- fastmcp
	- Core MCP framework for tool/resource/prompt registration

No additional runtime dependencies are currently required.

## Safety And Scope

- Read-only operations only
- No shell execution from tool handlers
- No arbitrary code execution of repository files
- Bounded file reads to avoid oversized responses

## Typical Workflow

1. Client calls find_entry_points_tool to identify likely startup files.
2. Client calls summarize_files_tool on top-ranked files.
3. Client fetches project://architecture for stable project context.
4. Client calls generate_onboarding_summary to produce first-day guidance.

## Notes For Extensibility

- Heuristics can be expanded per language ecosystem.
- Resources can be added for setup, conventions, or deployment docs.
- Prompt templates can be specialized for onboarding, handoff, or incident response.
