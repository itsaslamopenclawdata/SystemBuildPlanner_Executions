# Phased Roadmap: Architect's Cognitive Companion

## Goal

Build the system in small, validated phases. Each phase must produce a working learning outcome, not just documents.

---

## Phase 1: MVP — "Remember What I Learned"

**Time target:** 1 week  
**Focus:** Capture and retrieve architecture decisions

### Applications in MVP

1. **Learning Ingestion App** — read Obsidian notes and extract learning items
2. **Architecture Decision Memory App** — turn extracted items into ADRs
3. **Knowledge Graph Builder App** — link concepts, patterns, and projects

### MVP Outputs

- ADRs stored in Obsidian
- Simple knowledge graph queryable via CLI
- Ability to ask: *"What did I learn about caching?"*

### MVP Success Criteria

- At least 10 learning items ingested
- At least 5 ADRs created
- At least 3 queries return relevant results

---

## Phase 2: v2 — "Help Me Recall"

**Time target:** 1–2 weeks  
**Focus:** Active recall and spaced repetition

### Applications Added

4. **Spaced Repetition Coach App** — generate review prompts from knowledge graph

### v2 Outputs

- Daily review prompts pushed to the user
- Review schedule based on forgetting curve
- Weak-area identification

### v2 Success Criteria

- 1 review prompt generated per day
- User can mark prompts as known / hard / forgot
- System identifies top 3 weak topics weekly

---

## Phase 3: v3 — "Help Me Build"

**Time target:** 2–3 weeks  
**Focus:** Generate project blueprints from accumulated knowledge

### Applications Added

5. **Project Blueprint Generator App** — create starter architecture plans from memory

### v3 Outputs

- Blueprints include problem, requirements, applications, stack, risks
- Blueprints cite relevant ADRs and patterns from memory

### v3 Success Criteria

- Generate 3 blueprints for hypothetical projects
- Each blueprint references at least 3 prior ADRs
- User rates blueprint usefulness ≥ 7/10

---

## Phase 4: Scale — "Personal AI Workforce"

**Time target:** 4–6 weeks  
**Focus:** Automation, evaluation, and orchestration

### Capabilities Added

- Scheduled ingestion and reflection workflows
- Self-evaluation of generated blueprints
- Multi-agent orchestration with LangGraph
- MCP server exposing memory to other Hermes agents

### Scale Outputs

- End-to-end learning loop runs daily with minimal human input
- System feeds knowledge into other build projects

---

## Phase Progression Summary

```text
MVP  →  v2  →  v3  →  Scale
 │      │      │        │
Capture  Recall  Build   Automate
 │      │      │        │
3 apps   +1     +1      + workflows
```

Each phase reuses the previous phase's data and architecture.
