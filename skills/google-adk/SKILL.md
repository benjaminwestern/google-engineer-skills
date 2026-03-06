---
name: google-adk
version: "1.0.0"
description: Build AI agents with Google's ADK (Agent Development Kit) in Python, Go, Java, TypeScript. Use Application Default Credentials (ADC), single/multi-agent pipelines, tool integration, and secure deployment with Gemini models.
metadata:
  source_url: https://github.com/google/adk
  docs_url: https://google.github.io/adk-docs/
  languages: ["Python", "Go", "Java", "TypeScript"]
---

# Google ADK (Agent Development Kit) Guide

## Quick Start

**Python:**
```bash
# Using UV (recommended)
uv add google-adk

# Or with pip
pip install google-adk
```

**Dependency Management:**
- Use `pyproject.toml` for dependency management
- Generate `requirements.txt` when needed: `uv pip compile pyproject.toml -o requirements.txt`

**Go:**
```bash
go get google.golang.org/adk
go get google.golang.org/genai
```

**Python:**
```python
from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="researcher",
    model="gemini-2.5-flash",
    instruction="Research assistant with search capability.",
    tools=[google_search],
)
```

**Go:**
```go
package main

import (
    "context"
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/launcher/web"
    "google.golang.org/adk/model/gemini"
    "google.golang.org/genai"
)

func main() {
    ctx := context.Background()
    model, _ := gemini.NewModel(ctx, "gemini-2.5-flash", &genai.ClientConfig{})
    
    agent, _ := llmagent.New(llmagent.Config{
        Name:        "researcher",
        Model:       model,
        Instruction: "Research assistant.",
    })
    
    web.NewLauncher().Launch(ctx, agent)
}
```

## Authentication (ADC - Application Default Credentials)

**Use Application Default Credentials (ADC)** - the standard for GCP authentication. No keys needed in production.

### How ADC Works

ADC automatically discovers credentials:
1. **Production** (Cloud Run, GKE, Agent Engine): Uses attached service account automatically
2. **Local Development**: `gcloud auth application-default login`

### Local Development

```bash
# One-time setup
gcloud auth application-default login
gcloud auth application-default set-quota-project PROJECT_ID
```

### Production Deployment

**No code changes needed.** ADC automatically uses the service account attached to your compute resource.

```python
from google.cloud import bigquery

# Works everywhere - local AND production
client = bigquery.Client(project=project_id)  # Uses ADC automatically
```

### Attaching Service Accounts

```bash
# Cloud Run
gcloud run deploy my-agent \
  --service-account=my-agent@project.iam.gserviceaccount.com

# GKE Workload Identity
# Annotate K8s SA with GCP SA: iam.gke.io/gcp-service-account=my-agent@project.iam.gserviceaccount.com
```

See [authentication.md](references/authentication.md) for WIF (multi-cloud), OAuth (user auth), and advanced patterns.

## Multi-Language Support

| Language | Package | Install |
|----------|---------|---------|
| Python | `google-adk` | `uv add google-adk` or `pip install google-adk` |
| Go | `google.golang.org/adk` | `go get google.golang.org/adk` |
| Java | `com.google.adk:google-adk` | Maven/Gradle |
| TypeScript | `@google/adk` | `npm install @google/adk` |

## Critical Rules

1. **Entry point MUST be `root_agent`** - module-level variable
2. **Every agent package needs `__init__.py`** with `from . import agent`
3. **Set `max_iterations` on `LoopAgent`** - prevents infinite loops
4. **Use `output_key` + `output_schema`** for structured data flow
5. **One agent = one responsibility** - split agents with 5+ tools
6. **Use ADC for auth** - No service account keys in production
7. **Attach service accounts to compute resources** - Cloud Run, GKE, Agent Engine

## Project Structure

```
my_agent/
├── my_agent/
│   ├── __init__.py          # Required: from . import agent
│   ├── agent.py             # Defines root_agent
│   ├── prompts.py           # Instruction strings (optional)
│   ├── tools.py             # Custom tools (optional)
│   └── sub_agents/          # Sub-agent packages (optional)
├── tests/
│   └── test_agent.py
├── pyproject.toml           # requires-python >=3.10
└── .env                     # GOOGLE_CLOUD_PROJECT only (no keys!)
```

## Agent Types

| Type | Use When | Pattern |
|------|----------|---------|
| **Agent/LlmAgent** | Single task, one LLM call | Basic building block |
| **SequentialAgent** | Steps must run in order | Pipeline A → B → C |
| **ParallelAgent** | Independent sub-tasks | Fan-out, then merge |
| **LoopAgent** | Iterative refinement | Producer + critic |
| **AgentTool** | On-demand delegation | Use agent as a tool |

### Single Agent (Python)

```python
from google.adk.agents import Agent

root_agent = Agent(
    name="assistant",
    model="gemini-2.5-flash",
    instruction="Help users with tasks. Be concise.",
    description="General purpose assistant",
    tools=[my_tool],
    output_schema=ResponseModel,
    output_key="response",
)
```

### Single Agent (Go)

```go
agent, _ := llmagent.New(llmagent.Config{
    Name:        "assistant",
    Model:       model,
    Instruction: "Help users with tasks.",
    Tools:       []tool.Tool{myTool},
})
```

### Sequential Pipeline

```python
from google.adk.agents import SequentialAgent

pipeline = SequentialAgent(
    name="research_pipeline",
    sub_agents=[researcher, summarizer, writer],
)
```

### Parallel Execution

```python
from google.adk.agents import ParallelAgent

parallel = ParallelAgent(
    name="multi_search",
    sub_agents=[
        web_searcher,   # output_key="web_results"
        doc_searcher,   # output_key="doc_results"
    ],
)
```

## Tools

### Function Tools (Python)

```python
def get_weather(city: str, units: str = "celsius") -> dict:
    """Get current weather for a city.

    Args:
        city: The city name.
        units: 'celsius' or 'fahrenheit'.

    Returns:
        dict with temperature and conditions.
    """
    return {"temperature": 22, "conditions": "sunny"}

agent = Agent(tools=[get_weather])
```

### Function Tools (Go)

```go
import "google.golang.org/adk/tool"

func getWeather(city string, units string) (map[string]interface{}, error) {
    return map[string]interface{}{
        "temperature": 22,
        "conditions":  "sunny",
    }, nil
}

weatherTool := tool.FromFunction(getWeather)
```

### Tools with ADC (BigQuery Example)

```python
from google.adk.tools import ToolContext
from google.cloud import bigquery
from google.auth import default

def query_bigquery(sql: str, project_id: str, tool_context: ToolContext) -> dict:
    """Query BigQuery using ADC credentials."""
    # ADC automatically finds credentials
    credentials, _ = default()
    client = bigquery.Client(project=project_id, credentials=credentials)
    
    # Validate for read-only
    access_level = tool_context.state.get("user:access_level", "read_only")
    if access_level == "read_only" and not sql.strip().upper().startswith("SELECT"):
        return {"error": "Read-only users can only execute SELECT queries"}
    
    results = client.query(sql).result()
    return {"rows": [dict(row) for row in results]}
```

### Built-in Tools

```python
from google.adk.tools import google_search

agent = Agent(tools=[google_search])
```

## State Management

| Prefix | Scope | Example |
|--------|-------|---------|
| (none) | Session-scoped | `state["cart"]` |
| `user:` | Cross-session | `state["user:preferences"]` |
| `app:` | Application-wide | `state["app:config"]` |
| `temp:` | Current turn only | `state["temp:result"]` |

```python
researcher = Agent(name="researcher", output_key="findings")
writer = Agent(name="writer", instruction="Write based on: {state[findings]}")
```

## Callbacks

```python
def before_tool(tool, args, tool_context) -> dict | None:
    """Validate inputs or auto-approve."""
    if tool.name == "bigquery_query":
        access_level = tool_context.state.get("user:access_level", "read_only")
        if access_level == "read_only" and not is_select_only(args["sql"]):
            return {"error": "Read-only users can only run SELECT queries"}
    return None

agent = Agent(before_tool_callback=before_tool)
```

## Testing

```python
import pytest
from google.adk.runners import InMemoryRunner
from google.genai import types

@pytest.mark.asyncio
async def test_agent():
    runner = InMemoryRunner(agent=root_agent, app_name="test")
    session = await runner.session_service.create_session(
        user_id="test_user", app_name="test"
    )
    content = types.Content(role="user", parts=[types.Part.from_text(text="Test")])
    events = []
    async for event in runner.run_async(
        user_id="test_user", session_id=session.id, new_message=content
    ):
        events.append(event)
    assert "expected" in events[-1].content.parts[0].text
```

## Running & Deployment

```bash
# Python - Interactive
adk run my_agent

# Python - Web UI (using UV - recommended)
uvx --from google-adk adk web my_agent

# Python - Web UI (if installed globally)
adk web my_agent

# Python - Cloud Run
adk deploy cloud_run --project=my-project --region=us-central1 my_agent

# Go - Run agent
go run main.go
```

## Key Design Rules

1. **Split agents with 5+ tools** into focused specialists
2. **Pass data via `output_key` + `output_schema`**
3. **Set `max_iterations` on every `LoopAgent`**
4. **Separate generation from evaluation**
5. **Write precise `description` fields**
6. **Use ADC for authentication** - No keys in production
7. **Attach service accounts to compute resources**
8. **Use WIF for multi-cloud** - Azure → GCP

## Decision Guide

```
Single task, one LLM? → Agent
Steps in order? → SequentialAgent
Independent tasks? → ParallelAgent
Iterative refinement? → LoopAgent (with max_iterations)
On-demand delegation? → AgentTool
Cross-cloud authentication? → Workload Identity Federation + ADC
User OAuth required? → OAuth 2.0 flow
Azure → GCP access? → WIF + ADC (no keys!)
```

## Resources

- **ADK Docs**: https://google.github.io/adk-docs/llms.txt
- **ADK Python**: https://github.com/google/adk-python
- **ADK Go**: https://github.com/google/adk-go
- **ADC Guide**: https://cloud.google.com/docs/authentication/application-default-credentials

## References

- [authentication.md](references/authentication.md) - ADC, WIF, OAuth patterns
- [safety.md](references/safety.md) - Guardrails, Model Armor, security
- [design-patterns.md](references/design-patterns.md) - 15 patterns, anti-patterns
- [tools-reference.md](references/tools-reference.md) - Advanced tool patterns
- [advanced-patterns.md](references/advanced-patterns.md) - Hierarchical workflows, deployment
- [evaluation.md](references/evaluation.md) - Testing, metrics
- [a2a-protocol.md](references/a2a-protocol.md) - Remote agents
- [go-patterns.md](references/go-patterns.md) - Go-specific implementations
- [python-samples.md](references/python-samples.md) - Python code examples
