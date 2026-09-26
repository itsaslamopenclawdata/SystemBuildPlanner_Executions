# Applications Overview: Bookmark Manager API

## Application List

| # | Application | Purpose |
|---|---|---|
| 1 | Orchestrator App | Handles the orchestrator concerns of the system |
| 2 | Ingestion App | Handles the ingestion concerns of the system |

## Agent Workforce

| Agent | Responsibility |
|---|---|
| Planner Agent | planners inputs and produces outputs |

## Connection Summary

| From | To | What Moves |
|---|---|---|
| User / CLI | First App | Raw input |
| First App | Next App | Processed intermediate |
| Last App | User / CLI | Final output |

## Complexity Notes

This is a **Level 6** system: API + database system. It deliberately limits the number of applications and agents to keep the learning focus sharp. The architecture can grow as you progress to higher levels.
