# Technical Stack: Architect's Cognitive Companion

## Stack Philosophy

- **Open-source first**
- **Local-first**
- **Progressive complexity**
- **One primary tool per concern**

---

## Core Stack

| Concern | MVP Choice | Scale Choice | Rationale |
|---|---|---|---|
| Language | Python 3.11+ | Python 3.11+ | Lingua franca for AI/ML |
| Agent orchestration | LangGraph | LangGraph + LangGraph Platform (optional) | Graph-based stateful agent workflows |
| LLM | Ollama (local) | Ollama / vLLM | Free, private, offline |
| Embedding model | `nomic-embed-text` via Ollama | Same or `sentence-transformers` | Local embeddings |
| Web framework | CLI only | FastAPI | No UI needed at MVP |
| Vector store | ChromaDB | Qdrant / Elasticsearch | Simple semantic search |
| Graph store | NetworkX (in-memory + JSON persist) | Neo4j | Queryable concept map |
| Structured data | SQLite / JSON | PostgreSQL | Metadata, review history |
| File storage | Obsidian vault | Obsidian vault + cloud backup | Human-readable source of truth |
| Scheduling | `schedule` or cron | APScheduler / Celery Beat | Daily review and ingestion |
| Configuration | Pydantic Settings | Same | Typed config |
| Testing | pytest | pytest + CI | Validation |
| Observability | Print / log files | OpenTelemetry + Prometheus | Metrics and tracing |

---

## Per-Application Stack

### 1. Learning Ingestion App

| Layer | Tool |
|---|---|
| Agent framework | LangGraph |
| LLM | Ollama (`llama3.1` or `mistral`) |
| Markdown parsing | `markdown-it-py` |
| File discovery | `pathlib`, `watchdog` (optional) |
| Output format | Pydantic models → JSON |

### 2. Architecture Decision Memory App

| Layer | Tool |
|---|---|
| Agent framework | LangGraph |
| LLM | Ollama |
| Storage | Obsidian vault `adr/` + ChromaDB |
| Templating | Jinja2 |
| Similarity search | ChromaDB |

### 3. Knowledge Graph Builder App

| Layer | Tool |
|---|---|
| Agent framework | LangGraph |
| LLM | Ollama |
| Graph store | NetworkX (MVP), Neo4j (scale) |
| Vector store | ChromaDB |
| Embedding | Ollama `nomic-embed-text` |

### 4. Spaced Repetition Coach App

| Layer | Tool |
|---|---|
| Agent framework | LangGraph |
| LLM | Ollama |
| Scheduling | SQLite + `schedule` / APScheduler |
| Algorithm | SM-2 variant |
| Output | Markdown to Obsidian |

### 5. Project Blueprint Generator App

| Layer | Tool |
|---|---|
| Agent framework | LangGraph |
| LLM | Ollama |
| Retrieval | ChromaDB + NetworkX/Neo4j |
| Diagrams | Mermaid syntax |
| Templating | Jinja2 |

---

## Integration / Interface Stack

| Interface | Technology |
|---|---|
| Human-to-system | Obsidian markdown + CLI |
| App-to-app (MVP) | LangGraph messages + shared JSON files |
| App-to-app (scale) | REST API via FastAPI |
| Memory-to-agents | ChromaDB + NetworkX/Neo4j + SQLite |
| Hermes ecosystem (future) | MCP server |
| Scheduling | Cron or APScheduler |

---

## Technology Choices Not Made Yet

| Decision | Options | When to Decide |
|---|---|---|
| Local LLM model | `llama3.1`, `mistral`, `qwen2.5`, `phi4` | After first benchmark on ADR extraction |
| Vector store | ChromaDB vs Qdrant | When retrieval latency becomes a concern |
| Graph store | NetworkX vs Neo4j | When entity count exceeds ~1,000 |
| Web UI | Streamlit vs Gradio vs none | After v3 if portfolio showcase is needed |

---

## Constraints

- **No paid cloud LLM APIs required.**
- **No Kubernetes required** at MVP.
- **Data remains local** unless explicitly backed up.
- **Every tool must have a clear, justified reason to exist.**
