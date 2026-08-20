# Success Metrics: Architect's Cognitive Companion

## Measurement Philosophy

Every phase must have measurable outcomes. Subjective "feels useful" is not enough.

---

## Phase 1: MVP Metrics

| Metric | Target | Measurement Method |
|---|---|---|
| Learning items ingested | ≥ 10 | Count JSON records |
| ADRs created | ≥ 5 | Count markdown files in `adr/` |
| ADR completeness | 100% | All template fields filled |
| Knowledge graph entities | ≥ 20 | Count graph nodes |
| Knowledge graph relations | ≥ 30 | Count graph edges |
| Query relevance | ≥ 70% | Precision@3 on 5 test queries |
| Ingestion confidence | ≥ 75% average | Logged confidence scores |

### MVP Success Criteria

- User can ask a natural-language question and get a relevant ADR or concept.
- At least 5 decisions are permanently recorded.
- At least 20 entities are connected in the graph.

---

## Phase 2: v2 Metrics

| Metric | Target | Measurement Method |
|---|---|---|
| Daily prompts generated | 1+ per day | Count prompts |
| Prompt review completion rate | ≥ 70% | Review log / prompts generated |
| Average prompt clarity | ≥ 4/5 | User rating |
| Weak topics identified weekly | 1–3 | Weekly report |
| Hard-topic recall improvement | ≥ 20% | Re-test after one week |

### v2 Success Criteria

- System generates prompts without manual intervention.
- User reviews most prompts.
- System surfaces at least one weak topic per week.

---

## Phase 3: v3 Metrics

| Metric | Target | Measurement Method |
|---|---|---|
| Blueprints generated | ≥ 3 | Count markdown files in `blueprints/` |
| Blueprint completeness | 100% | All template sections filled |
| Blueprint usefulness | ≥ 7/10 | User rating |
| ADR citations per blueprint | ≥ 3 | Count cited ADRs |
| Constraint fit | ≥ 80% | Manual check against constraints |
| Time to first blueprint | ≤ 10 minutes | Timer from idea input |

### v3 Success Criteria

- Blueprint Generator produces a complete, cited architecture plan in under 10 minutes.
- User rates blueprints as useful (≥ 7/10).
- Each blueprint reuses past decisions.

---

## Phase 4: Scale Metrics

| Metric | Target | Measurement Method |
|---|---|---|
| End-to-end loop runs daily | ≥ 90% uptime | Scheduler logs |
| MCP queries served | ≥ 10/day | MCP server logs |
| Reflection sessions completed | ≥ 1 per project | Reflection log |
| Blueprint prediction accuracy | ≥ 70% | Compare blueprint to actual build |
| Learning velocity | 5× baseline | Time-to-blueprint + retention + reuse |

### Scale Success Criteria

- System runs daily with minimal human input.
- Other Hermes agents can query ACC memory.
- Each completed project feeds new ADRs back into the system.

---

## Leading Indicators

Track these weekly to catch problems early:

| Indicator | Healthy Sign |
|---|---|
| Ingestion rate | Steady or increasing |
| ADR retrieval frequency | Used regularly |
| Prompt completion rate | ≥ 50% |
| User corrections | Decreasing over time |
| Extraction confidence | Increasing over time |

## Lagging Indicators

Track these monthly or quarterly:

| Indicator | Healthy Sign |
|---|---|
| Concept retention | Improving on re-tests |
| Project start speed | Decreasing over time |
| Repeated mistakes | Decreasing over time |
| Cross-project pattern reuse | Increasing over time |
| Portfolio architecture maturity | User can explain any system clearly |

---

## Anti-Metrics

Do not optimize for:

- Number of notes ingested (quality > quantity)
- Size of knowledge graph (density > node count)
- Number of prompts generated (completion > generation)
- Number of blueprints produced (usefulness > volume)
- Complexity of tech stack (simple > impressive)
