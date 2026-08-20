# Application 5: Project Blueprint Generator App

## Purpose

Generate starter architecture plans for new projects by retrieving and synthesizing relevant ADRs, patterns, tools, and lessons from memory.

## Problem Solved

Every new project currently starts from a blank page. The Blueprint Generator turns accumulated architecture memory into a concrete starting point, reducing reinvention and accelerating design.

## Inputs

| Input | Format | Source |
|---|---|---|
| Project idea / requirements | Markdown / natural language | User direct input |
| Relevant ADRs | Markdown | ADR Memory App (retrieval) |
| Relevant patterns and tools | Graph + text | Knowledge Graph Builder App |
| Past project blueprints | Markdown | Local blueprint archive |
| Constraints | JSON / text | User input (budget, latency, scale, stack) |

## Outputs

| Output | Format | Destination |
|---|---|---|
| Project blueprint | Markdown | Obsidian vault `blueprints/` folder |
| Cited ADR list | Markdown | Inside blueprint |
| Architecture diagram text | Mermaid / DOT | Inside blueprint |
| Risk register | Markdown table | Inside blueprint |
| Next-step checklist | Markdown task list | Inside blueprint |

## Blueprint Template

| Section | Content |
|---|---|
| Problem | What are we solving? |
| Requirements | Functional and non-functional requirements |
| Constraints | Time, budget, scale, compliance |
| Proposed Applications | List of AI applications and their roles |
| Proposed Stack | Languages, frameworks, databases, models |
| Architecture Diagram | Mermaid diagram |
| Design Decisions | Cited ADRs that support the design |
| Trade-offs | What was gained and lost |
| Risks | Technical and execution risks |
| Success Metrics | How to measure this project's success |
| Learning Plan | What the user will learn by building it |
| Next Steps | Immediate tasks to start implementation |

## Workflow

```text
1. Receive project idea and constraints from user
2. Expand idea into structured requirements (with LLM)
3. Query ADR Memory for relevant past decisions
4. Query Knowledge Graph for relevant concepts, tools, patterns
5. Synthesize proposed architecture
6. Generate Mermaid diagram
7. Identify trade-offs and risks
8. Add learning plan and next steps
9. Write blueprint markdown to Obsidian
10. Notify user
```

## AI Agent

| Attribute | Value |
|---|---|
| Name | **Blueprint Agent** |
| Type | Specialist |
| Model | Local open-source LLM via Ollama |
| Tools | Requirement expander, ADR retriever, graph querier, blueprint writer, diagram generator |

### Agent Responsibilities

1. Translate vague project ideas into structured requirements.
2. Find the most relevant ADRs and patterns from memory.
3. Synthesize an architecture that fits constraints.
4. Cite sources transparently.
5. Generate actionable next-step checklists.

## Technology

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Agent framework | LangGraph |
| LLM | Ollama |
| Retrieval | ChromaDB (ADRs) + NetworkX/Neo4j (graph) |
| Diagrams | Mermaid syntax inside markdown |
| Templating | Jinja2 |

## Data Requirements

- Indexed ADRs
- Populated knowledge graph
- Past blueprint archive for style/examples

## Human Interaction

- User provides project idea
- User reviews and edits blueprint
- User can request alternative architectures
- User marks blueprint as accepted / rejected / archived

## Testing

| Test | Method |
|---|---|
| Citation quality | Each decision links to a real ADR |
| Blueprint completeness | All template sections filled |
| Usefulness score | User rates blueprint 1–10 |
| Constraint fit | Proposed stack matches stated constraints |

## Dependencies

- ADR Memory App
- Knowledge Graph Builder App
- Local vector and graph stores

## Failure Handling

| Failure | Response |
|---|---|
| No relevant ADRs found | Use general best practices, warn user |
| Constraints conflict | Surface trade-off to user for decision |
| LLM produces bad architecture | User edits, system logs rejection reason |

## Observability

- Blueprints generated per week
- Average user usefulness rating
- Percentage of cited ADRs actually relevant
- Time to generate a blueprint
