# 5× Intelligence Mechanism: Architect's Cognitive Companion

## The Missing Piece

Most learning systems are **passive archives**: they store notes and let you search them. That improves access, but it does not improve intelligence.

The missing piece is a **closed feedback loop** that converts every learning event into:

1. **Structured memory** (not loose notes)
2. **Active recall** (not passive re-reading)
3. **Pattern recognition** (connections across projects)
4. **Reusable output** (blueprints for future builds)
5. **Self-correction** (learning from what was forgotten or misapplied)

This loop is the **5× intelligence mechanism**.

---

## The Five Loops

### Loop 1: Capture → Structure

| Without ACC | With ACC |
|---|---|
| Notes stay as raw markdown | Notes become ADRs, concepts, and relations |
| Value decays quickly | Value persists and compounds |
| Search is keyword-only | Search is semantic + structured |

**How it works:**
The Learning Ingestion App reads your Obsidian notes and extracts decision candidates and concept candidates. The ADR Agent turns those into structured Architecture Decision Records. The Graph Builder turns concepts into a knowledge graph.

**Intelligence gain:** You stop losing what you learned.

---

### Loop 2: Storage → Connection

| Without ACC | With ACC |
|---|---|
| Notes are isolated | Concepts are linked |
| You cannot see relationships | You can traverse `depends_on`, `used_in`, `contradicts` |
| Each project starts blank | Each project builds on prior patterns |

**How it works:**
The Knowledge Graph Builder extracts entities (concepts, patterns, tools, projects) and relations between them. You can query: *"Show me all tools related to agent orchestration that I have used in past projects."*

**Intelligence gain:** You see patterns that were previously hidden.

---

### Loop 3: Connection → Recall

| Without ACC | With ACC |
|---|---|
| You re-read notes when you remember they exist | The system prompts you to recall exactly what you need |
| Review is random | Review is spaced and difficulty-aware |
| Forgetting is invisible | Weak topics are flagged automatically |

**How it works:**
The Spaced Repetition Coach generates prompts from the knowledge graph. It schedules reviews using a forgetting-curve algorithm. It measures which topics you struggle with.

**Intelligence gain:** You remember more, with less effort.

---

### Loop 4: Recall → Build

| Without ACC | With ACC |
|---|---|
| New projects start from a blank page | New projects start from a blueprint grounded in your memory |
| You forget relevant past decisions | ADRs are cited automatically in new blueprints |
| You reuse patterns by accident | You reuse patterns by design |

**How it works:**
The Project Blueprint Generator retrieves relevant ADRs, patterns, and tools from memory and synthesizes a starter architecture for your next project.

**Intelligence gain:** You build faster and make fewer repeated mistakes.

---

### Loop 5: Build → Reflect → Improve

| Without ACC | With ACC |
|---|---|
| Lessons from builds are lost | Lessons are captured and fed back |
| The system does not learn | The system improves from outcomes |
| No feedback on predictions | Predicted trade-offs are compared with actual results |

**How it works:**
After a project, you (or a future Reflection Agent) compare the blueprint with what actually happened. Did the predicted trade-off hold? Did the chosen tool work? The result is written back as new ADRs and lessons, closing the loop.

**Intelligence gain:** The system gets smarter every cycle.

---

## Why This Is 5×, Not 2×

A 2× improvement would be better search or better notes. A 5× improvement requires compounding:

```text
Capture → Structure → Connect → Recall → Build → Reflect
         ↑___________________________________________|
```

Each loop multiplies the previous one because the output of one phase becomes the input to the next. Memory becomes patterns. Patterns become recall. Recall becomes build. Build becomes better memory.

---

## The Most Important Loop: Reflection

The Reflection loop is the multiplier. Without it, ACC is a sophisticated notebook. With it, ACC becomes a learning machine.

### Reflection Questions Asked After Every Project

1. What did the blueprint predict correctly?
2. What did it predict incorrectly?
3. What new decision should be recorded?
4. What new concept or relation was discovered?
5. What should the system ask me to review next?

### Reflection Outputs

- New ADRs
- Updated knowledge graph
- New review prompts
- Improved blueprint template
- Weak-area report

---

## Measuring the 5× Boost

| Baseline | With ACC | Target |
|---|---|---|
| Time to start a new project design | From blank page to first blueprint | 5× faster |
| Retention of architecture concepts | After 30 days | 5× better recall |
| Reuse of past decisions | Per project | 5× more citations |
| Discovery of cross-project patterns | Manual | Automated |
| Repeated mistakes | High | Decreasing over time |

---

## Future: From Personal Brain to AI Workforce Brain

Once ACC is stable, it can expose an MCP server. Then every other Hermes agent can:

- Retrieve relevant ADRs before making decisions
- Query the knowledge graph during planning
- Get review prompts to keep knowledge fresh
- Request blueprints for new builds

At that point, your personal cognitive companion becomes the **shared memory layer of your AI workforce**.
