# Inter-Application Communication: Architect's Cognitive Companion

## Communication Philosophy

Use the simplest pattern that works for each interaction. Start with direct file and in-process message passing. Add heavier infrastructure only when a phase demands it.

## Layered Communication Pattern

| Layer | Use Case | Technology in MVP | Technology at Scale |
|---|---|---|---|
| **Agent workflow** | One application coordinating its own steps | LangGraph state graph | LangGraph + checkpointing |
| **Application-to-application** | Passing structured candidates and results | In-process LangGraph messages + shared files | Message queue or REST |
| **Shared memory** | Persistent knowledge accessible to all apps | Obsidian vault + ChromaDB + NetworkX | PostgreSQL + Neo4j + Qdrant |
| **Tool/context sharing** | Exposing tools to other Hermes agents | Local Python module | MCP server |
| **External boundary** | User and other systems interacting with ACC | CLI + Obsidian notes | FastAPI + web UI |

---

## Detailed Communication Flows

### 1. Learning Ingestion App → Architecture Decision Memory App

| Attribute | Value |
|---|---|
| What moves | Decision candidates (JSON) |
| Pattern | LangGraph message + file drop |
| Data format | `{"title", "context", "options", "tentative_decision", "source_note", "confidence"}` |
| Trigger | Ingestion Agent classifies a note as decision-related |
| Reliability | Candidates queued in local JSON if ADR App is unavailable |

### 2. Learning Ingestion App → Knowledge Graph Builder App

| Attribute | Value |
|---|---|
| What moves | Concept candidates (JSON) |
| Pattern | LangGraph message + shared temp file |
| Data format | `{"entities": [...], "relations": [...], "source_note"}` |
| Trigger | Ingestion Agent classifies a note as concept-related |
| Reliability | Graph Builder reads queued JSON on next run |

### 3. Architecture Decision Memory App → Shared Memory

| Attribute | Value |
|---|---|
| What moves | Structured ADRs (markdown) + vector embeddings |
| Pattern | File write to Obsidian + vector DB insert |
| Storage | Obsidian vault `adr/` folder + ChromaDB collection |
| Trigger | ADR Agent completes an ADR |

### 4. Knowledge Graph Builder App → Shared Memory

| Attribute | Value |
|---|---|
| What moves | Entity/relation graph + embeddings |
| Pattern | Graph store write + vector DB insert |
| Storage | NetworkX (MVP) / Neo4j (scale) + ChromaDB |
| Trigger | Graph Builder completes a merge |

### 5. Shared Memory → Spaced Repetition Coach App

| Attribute | Value |
|---|---|
| What moves | Entities due for review, weak-topic signals |
| Pattern | Query API (local Python function in MVP; REST at scale) |
| Data format | List of entity objects + relations |
| Trigger | Scheduled daily run or user request |

### 6. Shared Memory → Project Blueprint Generator App

| Attribute | Value |
|---|---|
| What moves | Relevant ADRs + patterns + tools |
| Pattern | Retrieval call (vector + graph query) |
| Data format | List of ADRs + subgraph |
| Trigger | User submits a project idea |

### 7. All Apps → Human

| Attribute | Value |
|---|---|
| What moves | Prompts, blueprints, reports, review queues |
| Pattern | Markdown files in Obsidian + CLI output |
| Storage | Obsidian vault |
| Trigger | Daily cron, app completion, user request |

---

## Communication Diagram

```text
┌─────────────────────────────────────────────────────────────┐
│                      HUMAN INTERFACE                        │
│              Obsidian Vault + CLI / FastAPI                   │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ Markdown in / out
                              │
┌─────────────────────────────┼───────────────────────────────┐
│                             │                               │
│  ┌──────────────────────┐   │   ┌────────────────────────┐  │
│  │ Spaced Repetition    │   │   │ Project Blueprint      │  │
│  │ Coach App            │◄──┘   │ Generator App          │  │
│  └──────────┬───────────┘       └───────────┬────────────┘  │
│             │                                │               │
│             │  Query                         │  Retrieval    │
│             ▼                                ▼               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                  SHARED MEMORY LAYER                   │  │
│  │  Obsidian vault (source of truth)                      │  │
│  │  ChromaDB (vector embeddings)                          │  │
│  │  NetworkX / Neo4j (knowledge graph)                    │  │
│  │  SQLite / JSON (review history, metadata)              │  │
│  └────────────────────────────────────────────────────────┘  │
│             ▲                                ▲               │
│             │                                │               │
│             │ Write                          │ Write         │
│  ┌──────────┴──────────┐      ┌──────────────┴──────────┐   │
│  │ Architecture        │      │ Knowledge Graph         │   │
│  │ Decision Memory   │      │ Builder App             │   │
│  │ App                 │      │                         │   │
│  └──────────┬──────────┘      └───────────┬─────────────┘   │
│             ▲                             ▲                   │
│             │                             │                   │
│             └───────────┬───────────────┘                     │
│                         │                                     │
│            LangGraph message / JSON queue                     │
│                         │                                     │
│              ┌──────────┴──────────┐                        │
│              │ Learning Ingestion  │                        │
│              │ App                 │                        │
│              └─────────────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Communication Rules

1. **No direct database coupling between applications.** Each app owns its writes to shared memory but reads through query interfaces.
2. **Markdown is the universal interface to the human.** Every output the user sees is markdown-first.
3. **JSON is the machine-to-machine interface.** All internal structured communication uses JSON.
4. **Queue, do not block.** If a downstream app is down, the upstream app writes to a local queue.
5. **Obsidian is the source of truth.** Even vector and graph stores are rebuildable from the Obsidian vault.

---

## Future: MCP Exposure

At scale, ACC can expose its memory as an MCP (Model Context Protocol) server so other Hermes agents can:

- Query ADRs
- Retrieve relevant concepts
- Get review prompts
- Request blueprints

This turns ACC from a personal tool into a shared brain for the AI workforce.
