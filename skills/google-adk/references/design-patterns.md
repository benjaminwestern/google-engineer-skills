---
name: adk-design-patterns
version: "1.0.0"
description: Design patterns for Google ADK agents including sequential pipelines, fan-out/fan-in, reflection loops, dynamic routing, and guardrails.
metadata:
  source_url: https://google.github.io/adk-docs/
  docs_url: https://google.github.io/adk-docs/patterns
---

# Design Patterns for ADK Agents

## Pattern Selection Guide

| Situation | Pattern | Implementation |
|-----------|---------|----------------|
| Task has multiple dependent steps | Sequential pipeline | `SequentialAgent` with ordered sub-agents |
| Sub-tasks are independent | Fan-out / Fan-in | `ParallelAgent` → merger Agent |
| Output quality must be high | Reflection loop | `LoopAgent` with producer + critic |
| Diverse inputs need different handling | Dynamic routing | Parent Agent with sub_agents |
| Procedure unknown at design time | Dynamic planning | Planning agent writes plan to state |
| Tool calls may fail | Layered fallback | SequentialAgent: primary → fallback |
| Safety/compliance required | Guardrails | `before_model_callback` + `before_tool_callback` |
| Budget constraints exist | Resource tiering | Different `model` per agent |
| Cross-session memory needed | Long-term memory | `MemoryService` |
| Human approval required | Human-in-the-loop | Escalation tools + callback gates |

## Core Execution Patterns

### Sequential Pipeline (Prompt Chaining)

Break complex tasks into focused sub-tasks. Each step has ONE responsibility.

**Rules:**
- Use structured output (Pydantic via `output_key`) between steps
- Insert validation between steps via callbacks
- Each agent reads upstream results from `state["key"]`

```python
root = SequentialAgent(
    name="pipeline",
    sub_agents=[
        extract_agent,      # output_key="extracted"
        validate_agent,     # reads state["extracted"]
        synthesize_agent,   # output_key="result"
    ]
)
```

### Fan-out / Fan-in (Parallelization)

Run independent tasks concurrently, then synthesize.

**Rules:**
- Each parallel agent MUST write to unique `output_key`
- Place synthesis agent AFTER parallel stage
- Only parallelize truly independent tasks

```python
root = SequentialAgent(
    name="workflow",
    sub_agents=[
        ParallelAgent(
            name="parallel",
            sub_agents=[
                agent_a,    # output_key="result_a"
                agent_b,    # output_key="result_b"
            ]
        ),
        merger,             # reads state["result_a"] and state["result_b"]
    ]
)
```

### Reflection (Producer-Critic Loop)

Generate output, evaluate, refine based on feedback.

**Rules:**
- Use SEPARATE critic agent (same-agent self-review = bias)
- Give critic specific evaluation criteria
- Set `max_iterations` (2-5) on LoopAgent
- Use `output_key` to pass data via state

```python
loop = LoopAgent(
    name="refinement",
    max_iterations=3,
    sub_agents=[producer, critic],
)
```

### Dynamic Routing

Direct flow to specialized sub-agents based on input.

**Rules:**
- Coordinator's instruction must list routing rules
- Each sub-agent's `description` drives Auto-Flow
- Include fallback/unclear handler
- Keep coordinator focused: classify → delegate → return

```python
coordinator = Agent(
    name="router",
    instruction="""Analyze and delegate:
    - Billing questions → billing_agent
    - Technical issues → tech_agent
    - Unclear → general_agent""",
    sub_agents=[billing_agent, tech_agent, general_agent],
)
```

## Robustness Patterns

### Error Handling & Recovery

Three-phase pipeline: **Detect → Handle → Recover**

```python
robust_agent = SequentialAgent(
    name="robust",
    sub_agents=[
        primary_handler,    # Attempts main approach
        fallback_handler,   # Checks state["primary_failed"]
        response_agent,     # Synthesizes or apologizes
    ]
)
```

### Human-in-the-Loop (HITL)

Define explicit escalation rules. Don't let agents decide ad hoc.

**Escalation triggers:**
- Agent confidence below threshold
- Tool failure after retry exhaustion
- Financial transactions above limit
- Content flagged as ambiguous
- Task requires ethical/legal judgment

```python
def escalate_to_human(reason: str, context: str, tool_context: ToolContext) -> dict:
    """Escalate to human for approval."""
    tool_context.state["escalation"] = {"reason": reason, "context": context}
    return {"status": "escalated", "message": "Waiting for human approval"}
```

### Guardrails & Safety

Layered defense - never rely on single mechanism.

| Stage | Mechanism | Purpose |
|-------|-----------|---------|
| Input validation | `before_model_callback` | Block prompt injection |
| Output filtering | `after_model_callback` | Catch toxicity |
| Tool parameter check | `before_tool_callback` | Prevent unauthorized actions |
| Behavioral constraints | Agent `instruction` | Define role boundaries |

```python
def content_guardrail(callback_context, llm_request):
    """Block unsafe requests."""
    if is_unsafe(llm_request.contents[-1]):
        return Content(role="model", parts=[Part.from_text("I cannot process this.")])
    return None  # Proceed

agent = Agent(before_model_callback=content_guardrail)
```

## Optimization Patterns

### Resource-Aware Model Selection

| Task Type | Model Tier | Example |
|-----------|-----------|---------|
| Simple factual queries | Fast/cheap (Flash) | "Capital of France?" |
| Complex reasoning | Powerful (Pro) | Multi-step analysis |
| Current events | Medium + search | "Today's market news" |

```python
# Router classifies, delegates to tiered workers
router = Agent(model="gemini-2.5-flash", sub_agents=[
    Agent(name="fast", model="gemini-2.5-flash"),
    Agent(name="powerful", model="gemini-2.5-pro"),
])
```

### Context Engineering

Design complete informational environment before token generation.

**Context layers:**
1. **System prompt** (`instruction`): Foundational rules
2. **Retrieved data**: Tool outputs, RAG results
3. **Implicit data**: User identity, history (injected via `before_model_callback`)

```python
def inject_context(callback_context, llm_request):
    """Add user context before model call."""
    user_tier = callback_context.state.get("user:tier", "free")
    llm_request.contents.insert(0, Content(
        role="system",
        parts=[Part.from_text(f"User tier: {user_tier}")]
    ))
```

## Universal Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| God Agent | Single agent with 10+ tools | Split into specialists |
| Self-review bias | Same agent generates and evaluates | Separate producer + critic |
| Monolithic prompt | All instructions in one prompt | Decompose into SequentialAgent |
| Unstructured handoff | Free-text between stages | Structured JSON via `output_key` |
| No validation gates | Errors cascade | `after_agent_callback` checks |
| Unbounded loops | LoopAgent without termination | Always set `max_iterations` |
| Missing fallback | Ambiguous inputs misrouted | Include unclear handler |
| Context overload | Full history in every prompt | Summarize, use state |
| One-model-fits-all | Expensive model for every query | Route by complexity |
| Silent tool failure | Agent proceeds as if success | Return structured error dicts |
| Direct state mutation | Modifying session.state directly | Use `output_key` or EventActions |

## State Management Best Practices

| Prefix | Scope | Persistence |
|--------|-------|-------------|
| (none) | Current session only | Session-scoped |
| `user:` | Tied to user ID | Cross-session for user |
| `app:` | Shared across all users | Application-wide |
| `temp:` | Current turn only | Not persisted |

**Rules:**
- Use `output_key` on agents to auto-save responses
- Use `tool_context.state` for complex updates in tools
- State changes only persist via `session_service.append_event()`
- Use serializable types only (str, int, bool, list, dict)
