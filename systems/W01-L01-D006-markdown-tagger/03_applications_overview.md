# Applications Overview: Markdown Tagger

## Application List

| # | Application | Purpose |
|---|---|---|
| 1 | Orchestrator App | Handles the orchestrator concerns of the system |

## Agent Workforce

| Agent | Responsibility |
|---|---|
| None | This level uses deterministic code or a simple LLM workflow |

## Connection Summary

| From | To | What Moves |
|---|---|---|
| User / CLI | First App | Raw input |
| First App | Next App | Processed intermediate |
| Last App | User / CLI | Final output |

## Complexity Notes

This is a **Level 1** system: Single-function tool or script. It deliberately limits the number of applications and agents to keep the learning focus sharp. The architecture can grow as you progress to higher levels.
