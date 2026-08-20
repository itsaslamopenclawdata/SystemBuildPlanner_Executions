# Application 4: Spaced Repetition Coach App

## Purpose

Generate review prompts from the knowledge graph and schedule them using a forgetting-curve model to maximize long-term retention.

## Problem Solved

Without active recall, architecture concepts fade. Reading notes is not enough. Spaced repetition turns passive learning into durable understanding.

## Inputs

| Input | Format | Source |
|---|---|---|
| Knowledge graph | Graph + embeddings | Knowledge Graph Builder App |
| ADR metadata | JSON / markdown | ADR Memory App |
| User performance history | JSON | Local store |
| Weak-topic signals | JSON | Self-computed from review history |

## Outputs

| Output | Format | Destination |
|---|---|---|
| Daily review prompts | Markdown | Obsidian daily note / CLI |
| Performance update | JSON | Local store |
| Weak-topic report | Markdown | Weekly Obsidian note |
| Review schedule | JSON | Local store |

## Prompt Types

| Type | Example |
|---|---|
| Concept recall | *"What is the difference between RAG and fine-tuning?"* |
| Decision recall | *"Why did we choose Redis over Memcached for caching?"* |
| Connection recall | *"Name three tools related to agent orchestration."* |
| Application prompt | *"When would you use event-driven architecture over REST?"* |

## Workflow

```text
1. Query knowledge graph for entities due for review
2. Generate prompts from entity + relations + ADRs
3. Rank prompts by predicted difficulty and importance
4. Present daily review set to user
5. Capture user response: easy / good / hard / forgot
6. Update next review date using forgetting curve
7. Update weak-topic report
8. Write review log to Obsidian
```

## AI Agent

| Attribute | Value |
|---|---|
| Name | **Coach Agent** |
| Type | Specialist |
| Model | Local open-source LLM via Ollama |
| Tools | Prompt generator, scheduler, difficulty estimator, report writer |

### Agent Responsibilities

1. Generate clear, answerable review prompts from the graph.
2. Estimate prompt difficulty.
3. Schedule reviews based on user performance.
4. Identify weak topics that need reinforcement.
5. Write weekly learning reports.

## Technology

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Agent framework | LangGraph |
| LLM | Ollama |
| Scheduling | Simple SM-2-like algorithm (MVP), Anki-compatible format (scale) |
| Storage | SQLite or JSON for review history |
| Output | Markdown to Obsidian |

## Data Requirements

- Review history per entity
- Forgetting curve parameters
- User performance tags

## Human Interaction

- User receives daily prompts (via Obsidian note or CLI)
- User grades each prompt
- User can request extra prompts on a topic

## Testing

| Test | Method |
|---|---|
| Prompt quality | User rates clarity 1–5 |
| Scheduling correctness | Hard items return sooner than easy items |
| Weak-topic detection | Known weak topic appears in weekly report |

## Dependencies

- Knowledge Graph Builder for entities and relations
- ADR Memory for decision-based prompts
- Local review history store

## Failure Handling

| Failure | Response |
|---|---|
| Empty knowledge graph | Generate simple prompts from ADRs instead |
| User misses a day | Carry over due prompts, do not reset schedule |
| LLM prompt generation fails | Use pre-defined template-based prompts |

## Observability

- Prompts generated per day
- Review completion rate
- Average difficulty rating
- Number of weak topics
- Retention trend over time
