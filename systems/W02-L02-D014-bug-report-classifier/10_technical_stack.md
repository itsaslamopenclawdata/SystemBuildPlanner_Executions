# Technical Stack: Bug Report Classifier

## Core Stack

- Python 3.11+
- LangGraph (for agent workflows)

## Stack Rationale

This stack is chosen to satisfy Level 2 requirements while staying open-source and locally runnable. Higher levels add components only when they solve a real problem.

## Alternatives Considered

| Component | Chosen | Alternative | Why Chosen |
|---|---|---|---|
| Language | Python | TypeScript | Ecosystem for AI/ML |
| LLM | Ollama | OpenAI API | Free, private, offline |
| Vector DB | ChromaDB | Qdrant | Simplicity at small scale |
