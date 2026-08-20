# Data Model: Architect's Cognitive Companion

## Core Entities

### 1. LearningItem

Represents a raw piece of learning extracted from input.

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Unique identifier |
| `source_path` | string | Path to source note |
| `source_type` | enum | `obsidian`, `manual`, `code`, `web`, `reflection` |
| `raw_text` | string | Original content |
| `categories` | list[string] | `decision`, `concept`, `reflection`, `project` |
| `confidence` | float | Agent confidence (0.0–1.0) |
| `extracted_at` | datetime | When extracted |
| `review_status` | enum | `pending`, `processed`, `flagged` |

### 2. ArchitectureDecisionRecord (ADR)

Structured record of an architecture decision.

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Unique identifier |
| `slug` | string | URL-friendly title |
| `title` | string | Decision title |
| `date` | date | Decision date |
| `status` | enum | `proposed`, `accepted`, `deprecated`, `superseded` |
| `context` | string | Problem context |
| `options` | list[string] | Alternatives considered |
| `decision` | string | Chosen option |
| `reason` | string | Why it was chosen |
| `trade_offs` | string | Gains and losses |
| `consequences` | string | Expected outcomes |
| `related_adrs` | list[UUID] | Linked ADRs |
| `source_items` | list[UUID] | Learning items that fed this ADR |
| `embedding_id` | string | Reference in vector store |

### 3. Entity (Knowledge Graph Node)

Represents a concept, pattern, tool, project, or lesson.

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Unique identifier |
| `name` | string | Human-readable name |
| `type` | enum | `concept`, `pattern`, `tool`, `project`, `lesson`, `decision` |
| `description` | string | Short description |
| `aliases` | list[string] | Alternative names |
| `embedding_id` | string | Reference in vector store |

### 4. Relation (Knowledge Graph Edge)

Connects two entities.

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Unique identifier |
| `source_id` | UUID | Source entity |
| `target_id` | UUID | Target entity |
| `relation_type` | enum | `relates_to`, `used_in`, `depends_on`, `contradicts`, `leads_to` |
| `confidence` | float | Extraction confidence |
| `source_item` | UUID | Learning item that produced this relation |

### 5. ReviewPrompt

A spaced-repetition prompt generated for the user.

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Unique identifier |
| `entity_id` | UUID | Related entity |
| `prompt_text` | string | The question |
| `answer_text` | string | Expected answer |
| `prompt_type` | enum | `concept`, `decision`, `connection`, `application` |
| `difficulty` | float | Estimated difficulty |
| `due_date` | date | Next review date |
| `status` | enum | `new`, `reviewed`, `mastered`, `lapsed` |

### 6. ReviewLog

Tracks user performance on review prompts.

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Unique identifier |
| `prompt_id` | UUID | Related prompt |
| `rating` | enum | `easy`, `good`, `hard`, `forgot` |
| `reviewed_at` | datetime | When reviewed |
| `next_due_date` | date | Calculated next review date |

### 7. ProjectBlueprint

Generated architecture plan for a new project.

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Unique identifier |
| `title` | string | Project title |
| `problem` | string | Problem statement |
| `requirements` | string | Requirements |
| `constraints` | string | Constraints |
| `applications` | list[string] | Proposed applications |
| `stack` | string | Proposed technology stack |
| `diagram` | string | Mermaid diagram text |
| `decisions` | list[UUID] | Cited ADRs |
| `trade_offs` | string | Trade-offs |
| `risks` | string | Risks |
| `success_metrics` | string | Metrics |
| `learning_plan` | string | What will be learned |
| `next_steps` | list[string] | Task list |
| `status` | enum | `draft`, `accepted`, `rejected`, `archived` |

---

## Entity Relationship Diagram

```text
LearningItem (1) ────> (N) ArchitectureDecisionRecord
LearningItem (N) ────> (N) Entity
LearningItem (N) ────> (N) Relation

ArchitectureDecisionRecord (N) ────> (N) ArchitectureDecisionRecord (related)

Entity (N) ───relates_to/used_in/depends_on/contradicts/leads_to───> (N) Entity

Entity (1) ────> (N) ReviewPrompt
ReviewPrompt (1) ────> (N) ReviewLog

ArchitectureDecisionRecord (N) ────> (N) ProjectBlueprint (cited)
Entity (N) ────> (N) ProjectBlueprint (relevant)
```

---

## Storage Mapping

| Entity | Primary Store | Index / Cache |
|---|---|---|
| LearningItem | SQLite JSON | None |
| ADR | Obsidian markdown | ChromaDB vector index |
| Entity | Graph store (NetworkX/Neo4j) | ChromaDB vector index |
| Relation | Graph store | None |
| ReviewPrompt | SQLite | Due-date index |
| ReviewLog | SQLite | Entity performance index |
| ProjectBlueprint | Obsidian markdown | ChromaDB vector index |

---

## Key Indexes

| Index | Purpose |
|---|---|
| ADR vector index | Semantic search over decisions |
| Entity vector index | Semantic search over concepts |
| Review due-date index | Find prompts due today |
| Entity performance index | Identify weak topics |
| Blueprint vector index | Find similar past blueprints |
