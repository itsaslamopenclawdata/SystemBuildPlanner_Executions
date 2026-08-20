# System Overview: Architect's Cognitive Companion

## 1. System Name

**Architect's Cognitive Companion (ACC)**

## 2. Purpose

Help an aspiring AI/ML Solutions Architect build a personal, AI-powered memory and learning system that captures architecture knowledge, surfaces it when needed, and progressively generates better project blueprints from accumulated experience.

## 3. Problem Statement

When learning system design, agentic AI, and architecture at high velocity, three problems recur:

1. **Forgetting**: valuable lessons from past projects fade.
2. **Fragmentation**: notes, code, decisions, and reflections live in disconnected places.
3. **Reinvention**: every new project starts from scratch instead of building on prior thinking.

The system turns scattered learning into reusable architecture intelligence.

## 4. Target Users

| User | Role | Primary Need |
|---|---|---|
| Aslam (you) | Learner / Builder / Future AI Architect | Capture, connect, and reuse what I learn |
| Future team | Collaborator | Understand architecture decisions and project blueprints |
| Portfolio audience | Evaluator | See structured, production-minded system design thinking |

## 5. High-Level Inputs

| Input Type | Examples |
|---|---|
| Daily learning notes | Markdown notes, Obsidian entries, code snippets |
| Project artifacts | Architecture sketches, API designs, schemas |
| Decisions | Why X was chosen over Y, trade-offs accepted |
| Reflections | What worked, what failed, what to try next |
| External sources | Blog posts, papers, documentation, videos |

## 6. High-Level Outputs

| Output Type | Examples |
|---|---|
| Architecture Decision Records (ADRs) | Structured, searchable decisions |
| Knowledge graph | Connected concepts, patterns, tools, projects |
| Review prompts | Spaced-repetition questions for active recall |
| Project blueprints | Starting architecture for the next build |
| Progress reports | What was learned, reviewed, and applied |

## 7. System Boundaries

### In Scope

- Ingesting learning material from Obsidian vault and direct input
- Structuring architecture decisions
- Building a queryable knowledge graph
- Generating review prompts
- Generating project blueprints
- Tracking learning velocity metrics

### Out of Scope (for MVP)

- Multi-user collaboration
- Real-time sync across devices
- Public web interface
- Advanced evaluation frameworks
- Cloud deployment

## 8. Design Principles

1. **Open-source first**
2. **Local-first**: data lives in your Obsidian vault and local vector store
3. **Agent-minimal**: one specialist agent per application, not more
4. **Composable**: each application can work independently
5. **Progressive**: MVP is tiny; each phase adds measurable value
