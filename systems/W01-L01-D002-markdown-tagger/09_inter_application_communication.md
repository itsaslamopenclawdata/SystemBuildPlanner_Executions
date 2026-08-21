# Inter-Application Communication: Markdown Tagger

## Communication Patterns Used

- In-process function calls
- Shared JSON files

## Why These Patterns?

At Level 1, the simplest reliable pattern is chosen. We avoid message brokers, Kubernetes, or distributed tracing until the complexity genuinely demands them.

## Data Flow

```text
User/CLI → App 1 → App 2 → ... → Output
```

Each application communicates through well-defined JSON messages or function calls. The interface contract is documented in the data model.

## Communication Rules

1. Use the simplest pattern that works.
2. Prefer synchronous calls for short workflows.
3. Queue only when a downstream app is unreliable or slow.
4. Keep interfaces small and explicit.
