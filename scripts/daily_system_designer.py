#!/usr/bin/env python3
"""
Daily System Designer Cron Agent

Runs once per day and creates a new system design folder in the
SystemBuildPlanner_Executions repository.

- Complexity starts at Level 1 (very simple) and increases by one level each week.
- Over 10 weeks the designs progress from a single tool to a production-grade distributed system.
- Generated designs are committed and pushed to GitHub automatically.

Defaults:
  Start date: first run date (written to a config file)
  Run time:   scheduled externally (e.g. Windows Task Scheduler) at 06:00 local time
  Output:     markdown (.md) files only — no code

To switch to LLM-based generation, install and run Ollama, then set USE_LLM=True below.
"""

import datetime
import json
import os
import random
import re
import subprocess
import sys
from pathlib import Path
from typing import List

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------

REPO_ROOT = Path("C:/Users/itssh/SystemBuildPlanner_Executions")
CONFIG_PATH = REPO_ROOT / ".daily_designer_config.json"
USE_LLM = False  # Set to True if Ollama is installed and running
OLLAMA_MODEL = "llama3.1"

# ---------------------------------------------------------------------------
# IDEA BANK: 10 unique system domains per level (70 total)
# Each level increases architectural complexity.
# ---------------------------------------------------------------------------

SYSTEM_IDEAS = {
    1: [  # Single tool / script
        {"name": "Daily Habit Logger", "problem": "Track daily habits in a simple CLI.", "user": "Personal productivity enthusiast"},
        {"name": "Markdown Tagger", "problem": "Auto-tag markdown notes with simple keywords.", "user": "Note taker"},
        {"name": "URL Saver", "problem": "Save and categorize useful URLs.", "user": "Researcher"},
        {"name": "Code Snippet Collector", "problem": "Collect and search small code snippets.", "user": "Developer"},
        {"name": "Focus Timer", "problem": "Track focused work sessions.", "user": "Knowledge worker"},
        {"name": "Quote Archiver", "problem": "Store and retrieve inspirational quotes.", "user": "Writer"},
        {"name": "Flashcard Maker", "problem": "Turn notes into simple Q&A flashcards.", "user": "Student"},
        {"name": "Expense Recorder", "problem": "Log daily expenses from CLI.", "user": "Personal finance tracker"},
        {"name": "Book Note Taker", "problem": "Capture key takeaways from books.", "user": "Reader"},
        {"name": "Meeting Note Logger", "problem": "Quickly log meeting notes and action items.", "user": "Professional"},
    ],
    2: [  # Simple CLI app with one AI workflow
        {"name": "Smart Note Summarizer", "problem": "Summarize long notes automatically.", "user": "Busy learner"},
        {"name": "Email Reply Suggester", "problem": "Generate draft replies to common emails.", "user": "Professional"},
        {"name": "Daily Journal Expander", "problem": "Turn a short journal bullet into a reflective paragraph.", "user": "Personal growth practitioner"},
        {"name": "Documentation Translator", "problem": "Translate technical docs into plain English.", "user": "Junior developer"},
        {"name": "Bug Report Classifier", "problem": "Classify bug reports by severity and component.", "user": "QA engineer"},
        {"name": "Tweet Generator", "problem": "Turn a blog post into a thread draft.", "user": "Content creator"},
        {"name": "Error Explainer", "problem": "Explain error messages in plain language.", "user": "Developer"},
        {"name": "Code Commenter", "problem": "Generate comments for a function.", "user": "Developer"},
        {"name": "Reading Time Estimator", "problem": "Estimate reading time and extract key claims.", "user": "Researcher"},
        {"name": "Prompt Refiner", "problem": "Improve the clarity of an LLM prompt.", "user": "AI builder"},
    ],
    3: [  # Multi-step AI workflow
        {"name": "Research Brief Builder", "problem": "Find, summarize, and structure research on a topic.", "user": "Researcher"},
        {"name": "Blog Post Pipeline", "problem": "Turn an outline into a structured blog post draft.", "user": "Content creator"},
        {"name": "Code Review Prepper", "problem": "Summarize PR changes and flag risky areas.", "user": "Engineering lead"},
        {"name": "Decision Helper", "problem": "List options, pros/cons, and recommendation for a decision.", "user": "Product manager"},
        {"name": "Question Bank Builder", "problem": "Generate study questions from notes.", "user": "Educator"},
        {"name": "Customer Feedback Synthesizer", "problem": "Cluster feedback into themes and action items.", "user": "Product owner"},
        {"name": "Job Description Tailorer", "problem": "Tailor a resume/CV to a job description.", "user": "Job seeker"},
        {"name": "API Docs Builder", "problem": "Generate API docs from code and examples.", "user": "Backend developer"},
        {"name": "Weekly Review Generator", "problem": "Synthesize weekly notes into a review report.", "user": "Knowledge worker"},
        {"name": "Competitor Feature Mapper", "problem": "Extract and compare features from web pages.", "user": "Strategist"},
    ],
    4: [  # Single-agent system
        {"name": "Architecture Review Agent", "problem": "Review a design proposal and suggest improvements.", "user": "Aspiring architect"},
        {"name": "Code Explainer Agent", "problem": "Explain codebases and answer questions about them.", "user": "Developer"},
        {"name": "Test Writer Agent", "problem": "Generate unit tests for Python functions.", "user": "Developer"},
        {"name": "Refactoring Agent", "problem": "Suggest and explain refactoring opportunities.", "user": "Maintainer"},
        {"name": "Debugging Agent", "problem": "Guide a user through systematic debugging.", "user": "Developer"},
        {"name": "Interview Prep Agent", "problem": "Generate system design interview questions and hints.", "user": "Engineer"},
        {"name": "Doc Update Agent", "problem": "Detect code changes and propose doc updates.", "user": "Tech writer"},
        {"name": "Dependency Risk Agent", "problem": "Flag risky dependencies and suggest alternatives.", "user": "Engineering lead"},
        {"name": "Performance Tuning Agent", "problem": "Suggest optimizations for slow code.", "user": "Engineer"},
        {"name": "Security Review Agent", "problem": "Spot common security issues in code or design.", "user": "Engineer"},
    ],
    5: [  # Multi-agent system with shared memory
        {"name": "Research-to-Write Crew", "problem": "Agents research, outline, draft, and edit an article.", "user": "Content team"},
        {"name": "Code Crew", "problem": "Planner, coder, reviewer, and tester agents build a feature.", "user": "Solo developer"},
        {"name": "Daily Learning Crew", "problem": "Agents ingest, summarize, quiz, and reflect on daily learning.", "user": "Self-learner"},
        {"name": "Design Critique Crew", "problem": "Architect, security, cost, and ops agents critique a design.", "user": "System designer"},
        {"name": "Customer Support Crew", "problem": "Triage, solve, and escalate agents handle support tickets.", "user": "Support team"},
        {"name": "Project Planning Crew", "problem": "Agents decompose goals, estimate, and schedule tasks.", "user": "Project manager"},
        {"name": "Data Analysis Crew", "problem": "Cleaner, analyzer, visualizer, and storyteller agents analyze data.", "user": "Data scientist"},
        {"name": "Marketing Asset Crew", "problem": "Agents generate copy, visuals brief, and campaign plan.", "user": "Marketer"},
        {"name": "Incident Response Crew", "problem": "Detect, diagnose, remediate, and post-mortem agents respond to incidents.", "user": "SRE"},
        {"name": "Onboarding Crew", "problem": "Agents guide a new hire through docs, tasks, and Q&A.", "user": "People ops"},
    ],
    6: [  # API + database system
        {"name": "Personal Knowledge API", "problem": "Expose notes, ADRs, and concepts via a REST API.", "user": "Personal AI ecosystem"},
        {"name": "Bookmark Manager API", "problem": "Store, tag, and retrieve bookmarks with full-text search.", "user": "Researcher"},
        {"name": "Habit Tracker API", "problem": "Track habits and streaks via API and simple UI.", "user": "Self-improver"},
        {"name": "Task Management API", "problem": "CRUD tasks with priorities, deadlines, and status.", "user": "Productivity user"},
        {"name": "Note Repository API", "problem": "Store and search notes with versioning.", "user": "Knowledge worker"},
        {"name": "Flashcard API", "problem": "Manage flashcards and review sessions.", "user": "Learner"},
        {"name": "Expense Tracker API", "problem": "Log, categorize, and summarize expenses.", "user": "Personal finance user"},
        {"name": "Contact Memory API", "problem": "Store people, interactions, and context.", "user": "Networker"},
        {"name": "Recipe API", "problem": "Store, search, and meal-plan recipes.", "user": "Home cook"},
        {"name": "Reading List API", "problem": "Track books, notes, and reading status.", "user": "Reader"},
    ],
    7: [  # RAG system
        {"name": "Obsidian Q&A Assistant", "problem": "Answer questions from your Obsidian vault.", "user": "Knowledge worker"},
        {"name": "Document Compliance Checker", "problem": "Check documents against policy using retrieval.", "user": "Compliance officer"},
        {"name": "Codebase Q&A", "problem": "Answer questions about a code repository.", "user": "Developer"},
        {"name": "Research Paper Assistant", "problem": "Answer questions over a collection of papers.", "user": "Researcher"},
        {"name": "Customer Support RAG", "problem": "Answer support questions from knowledge base.", "user": "Support agent"},
        {"name": "Contract Analyzer", "problem": "Answer questions about contract clauses.", "user": "Legal operations"},
        {"name": "SOP Navigator", "problem": "Find the right standard operating procedure.", "user": "Operations team"},
        {"name": "Course Tutor", "problem": "Answer student questions over course materials.", "user": "Student"},
        {"name": "Medical Literature Assistant", "problem": "Answer clinicians' questions over guidelines.", "user": "Clinician (with safeguards)"},
        {"name": "Product Manual Assistant", "problem": "Answer user questions over product docs.", "user": "End user"},
    ],
    8: [  # MCP / external tool integration
        {"name": "AI Workforce Orchestrator", "problem": "Coordinate multiple specialist agents using MCP tools.", "user": "AI architect"},
        {"name": "Browser-Assisted Researcher", "problem": "Use browser tools to gather and synthesize information.", "user": "Analyst"},
        {"name": "File-System Coding Agent", "problem": "Read, write, and test code via filesystem tools.", "user": "Developer"},
        {"name": "Database Analyst Agent", "problem": "Query databases and generate reports via SQL tools.", "user": "Data analyst"},
        {"name": "Git-Powered Release Assistant", "problem": "Use Git tools to prepare release notes and checks.", "user": "DevOps engineer"},
        {"name": "Shell Automation Agent", "problem": "Run shell commands and interpret outputs safely.", "user": "Engineer"},
        {"name": "Calendar-Aware Planning Agent", "problem": "Read calendar and plan work blocks.", "user": "Knowledge worker"},
        {"name": "Email-Enabled Assistant", "problem": "Draft and summarize emails via email tools.", "user": "Executive"},
        {"name": "SlackOps Agent", "problem": "Answer questions and run commands via Slack.", "user": "Team"},
        {"name": "Web-Scraping Monitor Agent", "problem": "Monitor websites and alert via connected tools.", "user": "Operations"},
    ],
    9: [  # Evaluation + observability
        {"name": "RAG Evaluation Platform", "problem": "Systematically evaluate retrieval and answer quality.", "user": "AI engineer"},
        {"name": "Agent Benchmark Harness", "problem": "Run benchmark tasks and score agent performance.", "user": "Agent builder"},
        {"name": "LLM Output Judge", "problem": "Evaluate LLM outputs against rubrics and gold answers.", "user": "AI product team"},
        {"name": "Prompt Test Lab", "problem": "A/B test prompts and measure output quality.", "user": "Prompt engineer"},
        {"name": "Hallucination Detector", "problem": "Detect unsupported claims in generated answers.", "user": "AI safety engineer"},
        {"name": "Cost-Latency Monitor", "problem": "Track cost, latency, and quality of AI calls.", "user": "Platform engineer"},
        {"name": "Trace Review Workbench", "problem": "Inspect agent traces and identify failure modes.", "user": "AI architect"},
        {"name": "Regression Test Suite for Agents", "problem": "Catch agent regressions across versions.", "user": "QA engineer"},
        {"name": "Feedback Loop Collector", "problem": "Collect human feedback and retrain evaluations.", "user": "ML engineer"},
        {"name": "Production Guardrails System", "problem": "Block, log, and alert on risky AI outputs.", "user": "AI safety team"},
    ],
    10: [  # Production-grade distributed system
        {"name": "Personal AI Operating System", "problem": "A coordinated platform of agents, memory, and UIs.", "user": "Power user"},
        {"name": "Multi-Tenant Agent SaaS", "problem": "Run isolated agent teams for multiple users.", "user": "Enterprise customers"},
        {"name": "Real-Time AI Analytics Platform", "problem": "Ingest events, run agents, and serve insights at scale.", "user": "Data platform team"},
        {"name": "Autonomous DevOps Platform", "problem": "Detect, diagnose, and remediate production issues.", "user": "SRE team"},
        {"name": "Enterprise Knowledge Platform", "problem": "RAG + agents over enterprise documents with governance.", "user": "Enterprise"},
        {"name": "AI-Native Customer Support Platform", "problem": "End-to-end support with humans in the loop.", "user": "Support organization"},
        {"name": "Multi-Modal Content Factory", "problem": "Generate and review text, image, and video assets at scale.", "user": "Marketing org"},
        {"name": "Regulatory Document Intelligence Platform", "problem": "Process, analyze, and monitor regulatory docs.", "user": "Compliance org"},
        {"name": "Supply Chain Risk Intelligence System", "problem": "Aggregate signals, predict risks, and recommend actions.", "user": "Operations org"},
        {"name": "AI-Powered Research & Development Platform", "problem": "Accelerate R&D with retrieval, agents, and simulations.", "user": "R&D org"},
    ],
}

# ---------------------------------------------------------------------------
# COMPLEXITY PROGRESSION
# ---------------------------------------------------------------------------

COMPLEXITY_PARAMS = {
    1:  {"num_apps": 1, "num_agents": 0, "has_db": False, "has_api": False, "has_rag": False, "has_mcp": False, "has_eval": False, "distributed": False, "description": "Single-function tool or script"},
    2:  {"num_apps": 1, "num_agents": 0, "has_db": False, "has_api": False, "has_rag": False, "has_mcp": False, "has_eval": False, "distributed": False, "description": "Simple CLI app with one AI workflow"},
    3:  {"num_apps": 1, "num_agents": 0, "has_db": False, "has_api": False, "has_rag": False, "has_mcp": False, "has_eval": False, "distributed": False, "description": "Multi-step AI workflow"},
    4:  {"num_apps": 1, "num_agents": 1, "has_db": False, "has_api": False, "has_rag": False, "has_mcp": False, "has_eval": False, "distributed": False, "description": "Single-agent system"},
    5:  {"num_apps": 2, "num_agents": 2, "has_db": False, "has_api": False, "has_rag": False, "has_mcp": False, "has_eval": False, "distributed": False, "description": "Multi-agent system with shared memory"},
    6:  {"num_apps": 2, "num_agents": 1, "has_db": True,  "has_api": True,  "has_rag": False, "has_mcp": False, "has_eval": False, "distributed": False, "description": "API + database system"},
    7:  {"num_apps": 3, "num_agents": 2, "has_db": True,  "has_api": True,  "has_rag": True,  "has_mcp": False, "has_eval": False, "distributed": False, "description": "RAG-powered system"},
    8:  {"num_apps": 3, "num_agents": 2, "has_db": True,  "has_api": True,  "has_rag": True,  "has_mcp": True,  "has_eval": False, "distributed": False, "description": "MCP-enabled agent system"},
    9:  {"num_apps": 3, "num_agents": 2, "has_db": True,  "has_api": True,  "has_rag": True,  "has_mcp": True,  "has_eval": True,  "distributed": False, "description": "Evaluated and observable system"},
    10: {"num_apps": 4, "num_agents": 3, "has_db": True,  "has_api": True,  "has_rag": True,  "has_mcp": True,  "has_eval": True,  "distributed": True,  "description": "Production-grade distributed system"},
}

APP_NAMES = [
    "Orchestrator",
    "Ingestion",
    "Memory",
    "Retrieval",
    "Reasoning",
    "Generation",
    "Evaluation",
    "Interface",
]

AGENT_NAMES = [
    "Planner",
    "Researcher",
    "Synthesizer",
    "Critic",
    "Writer",
    "Coder",
    "Reviewer",
    "Evaluator",
]

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def load_config() -> dict:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_config(cfg: dict) -> None:
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)


def run_git(args: List[str], cwd: Path) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        text=True,
        capture_output=True,
    ).stdout


def generate_system_overview(name: str, problem: str, user: str, level: int, params: dict) -> str:
    return f"""# System Overview: {name}

## System Name

**{name}**

## Purpose

This system solves the problem of: **{problem}**

It is designed as a learning exercise at **Level {level}** — a {params['description']}.

## Target User

{user}

## Problem Statement

{problem} Currently, this is handled manually, inconsistently, or not at all. The system automates the core workflow while keeping the architecture simple enough to understand and extend.

## High-Level Inputs

| Input | Description |
|---|---|
| User request | What the user wants the system to do |
| Source data | Raw text, files, URLs, or structured data relevant to the task |
| Configuration | Model, style, or behavior preferences |

## High-Level Outputs

| Output | Description |
|---|---|
| Processed result | The main deliverable of the system |
| Logs / metadata | Trace of what happened and why |
| Feedback signal | Optional: how useful the output was |

## System Boundaries

### In Scope

- The core workflow described above
- Local CLI execution
- Markdown documentation of design decisions

### Out of Scope (for this level)

- Multi-user collaboration
- Cloud deployment
- Advanced observability (unless level requires it)
- Enterprise security features

## Design Principles

1. Open-source first
2. Local-first where possible
3. One responsibility per component
4. Start simple, add complexity only when justified
5. Every design decision must be explainable

## Learning Objectives

After building this system, you should be able to explain:

- Why this system has {params['num_apps']} application(s) and {params['num_agents']} AI agent(s)
- How data flows from input to output
- What trade-offs were made at this complexity level
- How this system prepares you for Level {min(10, level + 1)}
"""


def generate_roadmap(name: str, level: int) -> str:
    return f"""# Phased Roadmap: {name}

## Goal

Build the system in small, validated phases. Each phase should produce a working artifact.

## Phase 1: MVP

**Time target:** 1–2 days
**Focus:** Prove the core workflow works end-to-end.

### Deliverables

- Input parsing works
- Core processing works
- Output is produced and usable
- Basic tests pass

### Success Criteria

- At least one happy-path test passes
- Output quality is acceptable to the target user
- System can be run from CLI

## Phase 2: Harden

**Time target:** 2–3 days
**Focus:** Add validation, error handling, and basic observability.

### Deliverables

- Input validation
- Error handling for common failure cases
- Logging of key events
- Minor refactoring for clarity

### Success Criteria

- No silent failures
- Logs explain what happened
- Code is readable and testable

## Phase 3: Extend

**Time target:** 2–3 days
**Focus:** Add one meaningful improvement based on real usage.

### Deliverables

- One new capability or quality improvement
- Updated tests
- Updated documentation

### Success Criteria

- Improvement is measurable or demonstrable
- Tests cover the new capability
- You can explain the trade-off of the extension

## Learning Loop

After each phase:

1. What worked?
2. What was harder than expected?
3. What would you do differently at Level {min(10, level + 1)}?
4. What new ADR or lesson belongs in your Architect's Cognitive Companion?
"""


def generate_applications_overview(name: str, level: int, params: dict) -> str:
    apps = APP_NAMES[: params["num_apps"]]
    agents = AGENT_NAMES[: params["num_agents"]]

    app_rows = "\n".join(
        f"| {i+1} | {app} App | Handles the {app.lower()} concerns of the system |"
        for i, app in enumerate(apps)
    )

    agent_rows = "\n".join(
        f"| {agent} Agent | {agent.lower()}s inputs and produces outputs |"
        for agent in agents
    ) if agents else "| None | This level uses deterministic code or a simple LLM workflow |"

    return f"""# Applications Overview: {name}

## Application List

| # | Application | Purpose |
|---|---|---|
{app_rows}

## Agent Workforce

| Agent | Responsibility |
|---|---|
{agent_rows}

## Connection Summary

| From | To | What Moves |
|---|---|---|
| User / CLI | First App | Raw input |
| First App | Next App | Processed intermediate |
| Last App | User / CLI | Final output |

## Complexity Notes

This is a **Level {level}** system: {params['description']}. It deliberately limits the number of applications and agents to keep the learning focus sharp. The architecture can grow as you progress to higher levels.
"""


def generate_app_detail(name: str, app_name: str, app_index: int, level: int, params: dict) -> str:
    has_agent = app_index < params["num_agents"]
    agent_name = AGENT_NAMES[app_index] if has_agent else "None"

    db_section = "- Local JSON or SQLite for state" if params["has_db"] else "- In-memory or file-based state"
    api_section = "- FastAPI endpoint for external access" if params["has_api"] else "- CLI interface only"
    rag_section = "- ChromaDB for vector retrieval" if params["has_rag"] else ""
    mcp_section = "- MCP server/client for tool sharing" if params["has_mcp"] else ""

    return f"""# Application {app_index + 1}: {app_name} App — {name}

## Purpose

Handles the {app_name.lower()} concerns of the {name} system.

## Inputs

| Input | Source |
|---|---|
| Raw or processed input | Previous app or CLI |
| Configuration | Environment / config file |

## Outputs

| Output | Destination |
|---|---|
| Processed result | Next app or CLI |
| Logs | Local log file |

## Workflow

1. Receive input
2. Validate input
3. Execute the {app_name.lower()} logic
4. Produce output
5. Log result

## AI Agent

| Attribute | Value |
|---|---|
| Agent | {agent_name if has_agent else "None (deterministic code or simple LLM call at this level)"} |
| Skills | {app_name.lower()}, validation, output formatting |

## Technology

- Python 3.11+
- LangGraph (if agent-driven)
{db_section}
{api_section}
{rag_section}
{mcp_section}

## Testing

- Happy-path test
- Input validation test
- Output format test

## Failure Handling

| Failure | Response |
|---|---|
| Invalid input | Return clear error message |
| Processing error | Log error and return fallback output |
| Downstream unavailable | Queue or retry once |
"""


def generate_communication(name: str, level: int, params: dict) -> str:
    patterns = ["In-process function calls", "Shared JSON files"]
    if params["num_apps"] > 1:
        patterns.append("LangGraph message passing")
    if params["has_api"]:
        patterns.append("REST API calls")
    if params["has_mcp"]:
        patterns.append("MCP tool/context sharing")
    if params["distributed"]:
        patterns.append("Message queue / event bus")

    return f"""# Inter-Application Communication: {name}

## Communication Patterns Used

{chr(10).join(f"- {p}" for p in patterns)}

## Why These Patterns?

At Level {level}, the simplest reliable pattern is chosen. We avoid message brokers, Kubernetes, or distributed tracing until the complexity genuinely demands them.

## Data Flow

```text
User/CLI → App 1 → App 2 → ... → Output
```

Each application communicates through well-defined JSON messages or function calls. The interface contract is documented in the data model.

## Communication Rules

1. Use the simplest pattern that works.
2. Prefer synchronous calls for short workflows.
3. Queue only when a downstream app is unreliable or slow.
4. Keep interfaces small and explicit.
"""


def generate_stack(name: str, level: int, params: dict) -> str:
    items = ["Python 3.11+", "LangGraph (for agent workflows)"]
    if params["has_db"]:
        items.append("SQLite or PostgreSQL (database)")
    if params["has_api"]:
        items.append("FastAPI (API layer)")
    if params["has_rag"]:
        items.append("ChromaDB or Qdrant (vector store)")
        items.append("Ollama (local embeddings + LLM)")
    if params["has_mcp"]:
        items.append("MCP SDK (tool sharing)")
    if params["has_eval"]:
        items.append("Custom evaluation harness + metrics")
    if params["distributed"]:
        items.append("Redis or message queue")
        items.append("Docker Compose (local multi-service)")

    return f"""# Technical Stack: {name}

## Core Stack

{chr(10).join(f"- {item}" for item in items)}

## Stack Rationale

This stack is chosen to satisfy Level {level} requirements while staying open-source and locally runnable. Higher levels add components only when they solve a real problem.

## Alternatives Considered

| Component | Chosen | Alternative | Why Chosen |
|---|---|---|---|
| Language | Python | TypeScript | Ecosystem for AI/ML |
| LLM | Ollama | OpenAI API | Free, private, offline |
| Vector DB | ChromaDB | Qdrant | Simplicity at small scale |
"""


def generate_data_model(name: str, level: int, params: dict) -> str:
    return f"""# Data Model: {name}

## Core Entities

### Input

| Field | Type | Description |
|---|---|---|
| id | string | Unique identifier |
| content | string | Raw input content |
| metadata | dict | Source, timestamp, tags |

### Output

| Field | Type | Description |
|---|---|---|
| id | string | Unique identifier |
| input_id | string | Reference to input |
| result | string | Generated result |
| confidence | float | Model confidence (0.0–1.0) |

{"### ReviewLog" if params["has_eval"] else ""}
{"| Field | Type | Description |" if params["has_eval"] else ""}
{"|---|---|---|" if params["has_eval"] else ""}
{"| id | string | Unique identifier |" if params["has_eval"] else ""}
{"| output_id | string | Reference to output |" if params["has_eval"] else ""}
{"| rating | enum | good / bad / neutral |" if params["has_eval"] else ""}

## Storage

{'- SQLite/PostgreSQL for structured data' if params["has_db"] else '- JSON or markdown files for simple persistence'}
- Obsidian vault for human-readable artifacts

## Notes

This data model is intentionally minimal at Level {level}. It grows as you add users, APIs, and evaluation.
"""


def generate_metrics(name: str, level: int, params: dict) -> str:
    return f"""# Success Metrics: {name}

## Phase Metrics

| Metric | Target | Measurement Method |
|---|---|---|
| Happy-path test passes | 100% | Automated test |
| Input handled correctly | ≥ 80% | Manual test set |
| Output is useful | ≥ 7/10 | Self-rating |
| System runs locally | Yes | Execution check |

## Level-Specific Metrics

{"| Vector retrieval precision | ≥ 70% | Top-3 relevance |" if params["has_rag"] else ""}
{"| MCP tool calls succeed | ≥ 90% | Tool execution logs |" if params["has_mcp"] else ""}
{"| Evaluation coverage | ≥ 5 test cases | Test suite count |" if params["has_eval"] else ""}
{"| Latency under load | < 1s p95 | Load test |" if params["distributed"] else ""}

## Anti-Metrics

- Do not optimize for lines of code
- Do not optimize for number of features
- Do not optimize for architectural complexity
"""


def generate_system_docs(name: str, problem: str, user: str, level: int, params: dict, folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)

    files = [
        ("01_system_overview.md", generate_system_overview(name, problem, user, level, params)),
        ("02_phased_roadmap.md", generate_roadmap(name, level)),
        ("03_applications_overview.md", generate_applications_overview(name, level, params)),
        ("09_inter_application_communication.md", generate_communication(name, level, params)),
        ("10_technical_stack.md", generate_stack(name, level, params)),
        ("11_data_model.md", generate_data_model(name, level, params)),
        ("12_success_metrics.md", generate_metrics(name, level, params)),
    ]

    for i in range(params["num_apps"]):
        app_name = APP_NAMES[i]
        files.append((f"04_app_{i+1:02d}_{app_name.lower()}.md", generate_app_detail(name, app_name, i, level, params)))

    for filename, content in files:
        with open(folder / filename, "w", encoding="utf-8") as f:
            f.write(content)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main() -> int:
    today = datetime.date.today()
    cfg = load_config()

    start_date_str = cfg.get("start_date")
    if start_date_str:
        start_date = datetime.date.fromisoformat(start_date_str)
    else:
        start_date = today
        cfg["start_date"] = today.isoformat()
        save_config(cfg)

    day_index = (today - start_date).days
    week = day_index // 7 + 1
    level = min(10, week)
    day_in_week = day_index % 7 + 1

    print(f"Today: {today} | Start: {start_date} | Day index: {day_index} | Week: {week} | Level: {level} | Day in week: {day_in_week}")

    # Select a deterministic-but-unique system for this day
    ideas = SYSTEM_IDEAS[level]
    seed = int(today.strftime("%Y%m%d"))
    rng = random.Random(seed)
    idea = ideas[rng.randint(0, len(ideas) - 1)]
    name = idea["name"]

    slug = slugify(name)
    folder_name = f"W{week:02d}-L{level:02d}-D{day_index + 1:03d}-{slug}"
    folder = REPO_ROOT / "systems" / folder_name

    params = COMPLEXITY_PARAMS[level]

    print(f"Generating system: {name}")
    print(f"Folder: {folder}")

    generate_system_docs(name, idea["problem"], idea["user"], level, params, folder)

    # Update main README with latest system
    readme_path = REPO_ROOT / "README.md"
    with open(readme_path, "r", encoding="utf-8") as f:
        readme = f.read()

    new_entry = f"| `systems/{folder_name}` | {name} | Level {level} — {params['description']} | Planned |\n"
    if "## Systems" not in readme:
        readme += "\n## Systems\n\n| Folder | System | Level | Status |\n|---|---|---|---|\n" + new_entry
    else:
        if folder_name not in readme:
            readme = readme.replace(
                "| Folder | System | Level | Status |\n|---|---|---|---|\n",
                "| Folder | System | Level | Status |\n|---|---|---|---|\n" + new_entry,
            )

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme)

    # Commit and push
    try:
        run_git(["add", "-A"], REPO_ROOT)
        run_git(["commit", "-m", f"Add daily system design: {folder_name}"], REPO_ROOT)
        run_git(["push", "origin", "main"], REPO_ROOT)
        print("Committed and pushed successfully.")
    except subprocess.CalledProcessError as e:
        print("Git operation failed:", e.stderr, file=sys.stderr)
        return 1

    print(f"Done: https://github.com/itsaslamopenclawdata/SystemBuildPlanner_Executions/tree/main/systems/{folder_name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
