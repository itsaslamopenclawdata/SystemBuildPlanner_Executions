# Application 3: Knowledge Graph Builder App

## Purpose

Extract concepts, patterns, tools, and projects from learning inputs and connect them into a queryable knowledge graph.

## Problem Solved

Notes and ADRs are documents. Real understanding comes from seeing how ideas connect: *"Redis is related to caching, caching is related to performance, performance is related to the e-commerce project."*

## Inputs

| Input | Format | Source |
|---|---|---|
| Concept candidates | JSON | Learning Ingestion App |
| ADRs | Markdown | ADR Memory App |
| Manual entity/relation entries | JSON / markdown | User direct input |

## Outputs

| Output | Format | Destination |
|---|---|---|
| Knowledge graph | Graph data + embeddings | Local graph store |
| Entity/relation JSON | JSON | Shared memory |
| Graph query responses | JSON / markdown | Spaced Repetition Coach, Blueprint Generator, user |
| Visual graph export | `.dot` / `.html` | Obsidian attachments (optional) |

## Entity Types

| Type | Examples |
|---|---|
| Concept | Caching, vector search, agent orchestration |
| Pattern | Event-driven architecture, microservices, RAG |
| Tool | Redis, LangGraph, ChromaDB, FastAPI |
| Project | 100-agent system, ACC, e-commerce RAG |
| Decision | Chose Redis over Memcached |
| Lesson | Avoid premature optimization |

## Relation Types

| Relation | Example |
|---|---|
| `relates_to` | Redis relates_to Caching |
| `used_in` | LangGraph used_in 100-agent system |
| `depends_on` | RAG depends_on Vector Search |
| `contradicts` | Serverless contradicts Monolith (trade-off) |
| `leads_to` | Caching leads_to Lower Latency |

## Workflow

```text
1. Receive concept candidates from Ingestion App
2. Extract entities using LLM + rules
3. Extract relations between entities
4. Merge with existing graph
5. Resolve duplicates and conflicts
6. Embed entities and relations
7. Store in local graph + vector store
8. Expose query API
```

## AI Agent

| Attribute | Value |
|---|---|
| Name | **Graph Builder Agent** |
| Type | Specialist |
| Model | Local open-source LLM via Ollama |
| Tools | Entity extractor, relation extractor, graph merge tool, query tool |

### Agent Responsibilities

1. Identify entities in learning inputs.
2. Identify relationships between entities.
3. Merge new information without duplicating existing nodes.
4. Resolve conflicts when the same concept is described differently.
5. Answer graph queries: *"What tools are related to RAG?"*

## Technology

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Agent framework | LangGraph |
| LLM | Ollama |
| Graph store | NetworkX (MVP), Neo4j (scale) |
| Vector store | ChromaDB |
| Query | Cypher (Neo4j at scale) or NetworkX API |

## Data Requirements

- Entity schema
- Relation schema
- Embedding model (e.g., `nomic-embed-text` via Ollama)

## Human Interaction

- User can browse graph via simple CLI or Obsidian-linked notes
- User can correct entity/relation extractions
- User can query graph in natural language

## Testing

| Test | Method |
|---|---|
| Entity extraction accuracy | Compare extracted entities to manual labels |
| Relation extraction accuracy | Precision/recall on known relation pairs |
| Graph query correctness | Test 10 predefined queries |

## Dependencies

- Learning Ingestion App for concept candidates
- ADR Memory App for decision entities
- Vector store for embedding-based search

## Failure Handling

| Failure | Response |
|---|---|
| Relation extraction is low confidence | Store entity only, flag for review |
| Duplicate entity detected | Merge nodes and keep strongest relation |
| Graph store unavailable | Persist raw JSON to disk, retry later |

## Observability

- Number of entities and relations
- Graph density (edges / nodes)
- Query latency
- Extraction confidence distribution
