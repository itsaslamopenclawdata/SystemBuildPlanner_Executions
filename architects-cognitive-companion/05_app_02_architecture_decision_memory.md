# Application 2: Architecture Decision Memory App

## Purpose

Store, version, and retrieve Architecture Decision Records (ADRs) so that design choices are never lost and can be reused in future projects.

## Problem Solved

Architecture decisions are usually scattered across notes, meeting minutes, comments, and memory. When a similar problem arises, the reasoning is forgotten, leading to repeated mistakes or reinvented trade-offs.

## Inputs

| Input | Format | Source |
|---|---|---|
| Decision candidates | JSON | Learning Ingestion App |
| Manual ADR drafts | Markdown | User direct input |
| Existing ADRs | Markdown | Obsidian vault ADR folder |

## Outputs

| Output | Format | Destination |
|---|---|---|
| Structured ADRs | Markdown | Obsidian vault `adr/` folder |
| ADR metadata index | JSON | Local vector store |
| Search results | Markdown / JSON | User, Blueprint Generator App |
| Update notifications | Markdown | Obsidian daily notes |

## ADR Template

Each ADR contains:

| Field | Description |
|---|---|
| Title | Decision title |
| Date | Decision date |
| Status | Proposed / Accepted / Deprecated / Superseded |
| Context | What problem were we solving? |
| Options | Alternatives considered |
| Decision | What was chosen |
| Reason | Why this option was chosen |
| Trade-offs | What was gained and lost |
| Consequences | Expected outcomes |
| Related ADRs | Links to related decisions |

## Workflow

```text
1. Receive decision candidate from Ingestion App
2. Validate completeness against ADR template
3. Check for duplicates or related existing ADRs
4. If complete: generate ADR markdown
5. Write ADR to Obsidian vault
6. Index ADR metadata in vector store
7. Notify user of new / updated ADR
```

## AI Agent

| Attribute | Value |
|---|---|
| Name | **ADR Agent** |
| Type | Specialist |
| Model | Local open-source LLM via Ollama |
| Tools | ADR template validator, similarity searcher, markdown writer |

### Agent Responsibilities

1. Transform decision candidates into complete ADRs.
2. Detect duplicates and suggest merges.
3. Maintain ADR status lifecycle.
4. Answer retrieval queries like *"Why did we choose Redis over Memcached?"*
5. Provide relevant ADRs to the Blueprint Generator.

## Technology

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Agent framework | LangGraph |
| LLM | Ollama |
| Storage | Obsidian vault (markdown) + ChromaDB (vector index) |
| Search | Vector similarity + metadata filters |
| Templating | Jinja2 |

## Data Requirements

- ADR schema in Pydantic
- Vector embeddings of ADR content
- Backlinks to source notes

## Human Interaction

- User reviews proposed ADRs before acceptance (MVP)
- User can query ADRs via CLI
- User can mark ADRs as deprecated or superseded

## Testing

| Test | Method |
|---|---|
| ADR completeness | Check output has all required fields |
| Duplicate detection | Inject known duplicate, verify merge suggestion |
| Retrieval relevance | Query ADR store, measure precision@5 |

## Dependencies

- Learning Ingestion App for candidates
- Obsidian vault write access
- ChromaDB for vector index
- Knowledge Graph Builder for entity linking

## Failure Handling

| Failure | Response |
|---|---|
| Candidate is incomplete | Return to Ingestion Agent or flag for human review |
| Vector DB unavailable | Fall back to file-system text search |
| Duplicate detection fails | User manually resolves in review queue |

## Observability

- ADRs created per week
- ADR retrieval frequency
- Average retrieval relevance score
