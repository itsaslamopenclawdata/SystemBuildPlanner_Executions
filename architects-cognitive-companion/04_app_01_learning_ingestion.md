# Application 1: Learning Ingestion App

## Purpose

Capture raw learning inputs and convert them into structured artifacts that downstream applications can process.

## Problem Solved

Learning material arrives unstructured: Obsidian notes, code snippets, web articles, reflections, videos. The system needs a single entry point that normalizes these inputs into consistent learning items.

## Inputs

| Input | Format | Source |
|---|---|---|
| Obsidian markdown notes | `.md` files | `D:\HermesObsidian` vault |
| Manual text entries | Plain text / markdown | CLI or direct input |
| Code snippets | `.py`, `.json`, `.yaml`, etc. | Project folders |
| Web articles | URL or raw text | Browser / read-later tool |
| Reflections | Markdown or voice-to-text | End-of-day input |

## Outputs

| Output | Format | Destination |
|---|---|---|
| Structured learning items | JSON | In-memory + local store |
| Decision candidates | JSON | ADR Memory App |
| Concept candidates | JSON | Knowledge Graph Builder App |
| Ingestion log | Markdown | Obsidian vault log folder |

## Workflow

```text
1. Discover input sources (Obsidian folder, manual input, code folder)
2. Read content
3. Classify content type: decision, concept, reflection, project artifact
4. Extract metadata: topic, source, date, confidence
5. Produce structured learning items
6. Route candidates to appropriate downstream app
7. Write ingestion log to Obsidian
```

## AI Agent

| Attribute | Value |
|---|---|
| Name | **Ingestion Agent** |
| Type | Specialist |
| Model | Local open-source LLM via Ollama (e.g., `llama3.1`, `mistral`) |
| Tools | File reader, markdown parser, classifier, metadata extractor |

### Agent Responsibilities

1. Decide whether a note contains useful learning or noise.
2. Extract key claims, decisions, and concepts.
3. Assign confidence scores to extractions.
4. Route high-confidence decision candidates to the ADR Agent.
5. Route high-confidence concept candidates to the Graph Builder Agent.

## Technology

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Agent framework | LangGraph |
| LLM | Ollama (local) |
| Parsing | `markdown-it-py` or `beautifulsoup4` |
| Configuration | Pydantic Settings |
| Orchestration | LangGraph state graph |

## Data Requirements

- Read access to Obsidian vault
- Local temp directory for intermediate JSON
- Schema for learning items

## Human Interaction

- User can add manual inputs via CLI
- User can review ingestion log
- Low-confidence extractions are flagged for human review

## Testing

| Test | Method |
|---|---|
| Classification accuracy | Hand-label 20 notes, compare with agent output |
| Extraction completeness | Check that key decisions are not missed |
| Routing correctness | Verify decision candidates reach ADR app |

## Dependencies

- Obsidian vault path configured
- Ollama running with chosen model
- Downstream apps available to receive candidates

## Failure Handling

| Failure | Response |
|---|---|
| LLM unavailable | Fall back to deterministic keyword-based extraction |
| Malformed markdown | Skip file and log error |
| Downstream app not running | Queue candidates in local JSON file |

## Observability

- Ingestion count per day
- Average extraction confidence
- Number of items queued vs. routed
