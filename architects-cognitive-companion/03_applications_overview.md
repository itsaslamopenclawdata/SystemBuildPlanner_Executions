# Applications Overview: Architect's Cognitive Companion

The system is decomposed into five AI applications. Each application owns one clear capability. They communicate through a layered pattern described in [10_inter_application_communication.md](./10_inter_application_communication.md).

---

## Application List

| # | Application | Purpose | MVP Phase |
|---|---|---|---|
| 1 | [Learning Ingestion App](./04_app_01_learning_ingestion.md) | Capture raw learning inputs and turn them into structured artifacts | MVP |
| 2 | [Architecture Decision Memory App](./05_app_02_architecture_decision_memory.md) | Store, version, and retrieve architecture decisions (ADRs) | MVP |
| 3 | [Knowledge Graph Builder App](./06_app_03_knowledge_graph_builder.md) | Extract concepts and connect them into a queryable graph | MVP |
| 4 | [Spaced Repetition Coach App](./07_app_04_spaced_repetition_coach.md) | Generate daily review prompts based on the knowledge graph | v2 |
| 5 | [Project Blueprint Generator App](./08_app_05_blueprint_generator.md) | Create starter architecture plans from accumulated memory | v3 |

---

## High-Level Connection Map

```text
┌─────────────────────────────────────────────────────────────────────┐
│                         EXTERNAL INPUTS                              │
│  Obsidian notes │ Code snippets │ Web articles │ Manual reflections   │
└───────────────────────┬───────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────┐
│  1. Learning Ingestion App         │
│  Extracts: decisions, concepts,    │
│  reflections, project metadata   │
└──────┬─────────────┬─────────────┘
       │             │
       ▼             ▼
┌────────────────┐  ┌──────────────────────────────┐
│ 2. ADR Memory  │  │ 3. Knowledge Graph Builder   │
│    App         │  │      App                     │
│ Stores: why X  │  │ Stores: entities + relations │
│ over Y         │  │                              │
└──────┬─────────┘  └──────┬───────────────────────┘
       │                   │
       ▼                   ▼
┌──────────────────────────────────┐
│  SHARED MEMORY LAYER             │
│  Obsidian vault + local vector DB│
│  + knowledge graph store         │
└──────────────────┬───────────────┘
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
┌──────────┐ ┌──────────┐ ┌──────────────┐
│ 4. Spaced│ │ 5. Blue- │ │ Future Apps  │
│ Repeti-  │ │ print    │ │ (Evaluation, │
│ tion     │ │ Generator│ │ Retrospect)  │
│ Coach    │ │          │ │              │
└──────────┘ └──────────┘ └──────────────┘
```

---

## Communication Summary

| From | To | What Moves | Pattern |
|---|---|---|---|
| Ingestion App | ADR Memory App | Extracted decision candidates | LangGraph message + file write |
| Ingestion App | Knowledge Graph App | Extracted entities and relations | LangGraph message + shared JSON |
| ADR Memory App | Shared Memory | Structured ADR markdown files | File I/O to Obsidian vault |
| Knowledge Graph App | Shared Memory | Entity/relation store | Vector + graph database writes |
| Shared Memory | Spaced Repetition Coach | Weak-topic signals + concepts | Query API (REST/local) |
| Shared Memory | Blueprint Generator | Relevant ADRs + patterns | Retrieval + graph query |
| All Apps | Human | Prompts, blueprints, reports | Markdown + CLI + Obsidian |

---

## Agent Workforce by Application

Each application uses one specialist agent.

| Application | Agent Role | Core Skills |
|---|---|---|
| Learning Ingestion | **Ingestion Agent** | Parsing markdown, extracting metadata, classifying content |
| Architecture Decision Memory | **ADR Agent** | Structuring decisions, versioning, conflict detection |
| Knowledge Graph Builder | **Graph Builder Agent** | Entity extraction, relation extraction, graph maintenance |
| Spaced Repetition Coach | **Coach Agent** | Question generation, scheduling, forgetting-curve logic |
| Project Blueprint Generator | **Blueprint Agent** | Architecture synthesis, requirement analysis, citation |

---

## Why Five Applications?

- **One responsibility per app** makes each one understandable and testable.
- **No app is forced to exist**: if an application can be removed without breaking value, we remove it.
- **Five is the minimum** to cover: capture → structure → connect → recall → build.
