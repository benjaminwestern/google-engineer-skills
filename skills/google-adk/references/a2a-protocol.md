---
name: adk-a2a-protocol
version: "1.0.0"
description: A2A (Agent-to-Agent) protocol for Google ADK including remote agent communication, discovery, and task delegation patterns.
metadata:
  source_url: https://google.github.io/adk-docs/
  docs_url: https://google.github.io/adk-docs/a2a
---

# A2A (Agent-to-Agent) Protocol

## When to Use A2A vs Local Sub-Agents

| Criteria | A2A (Remote) | Local Sub-Agents |
|----------|-------------|------------------|
| Deployment | Separate services, different machines | Same process |
| Teams | Different teams/organizations | Same team |
| Languages | Cross-language | Same language |
| Performance | Network overhead | Direct memory access |
| State | Isolated per agent | Shared session state |

**Use A2A when:**
- Agent runs as a separate standalone service
- Different teams maintain different agents
- Agents are in different languages/frameworks
- You need microservices architecture for agents

**Use local sub-agents when:**
- Agents share process and state
- Performance is critical (no network overhead)
- Simple internal code organization

## Installation

```bash
pip install google-adk[a2a]
```

## Exposing an Agent via A2A

### Method 1: `to_a2a()` (Recommended)

```python
from google.adk.agents import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a

root_agent = Agent(
    name="math_agent",
    model="gemini-2.5-flash",
    instruction="You solve math problems.",
    tools=[solve_equation],
)

a2a_app = to_a2a(root_agent, port=8001)
```

Run:

```bash
uvicorn my_agent.agent:a2a_app --host localhost --port 8001
```

Verify agent card:

```bash
curl http://localhost:8001/.well-known/agent-card.json
```

### Method 2: ADK CLI

```bash
adk api_server --a2a --port 8001 path/to/agent_folder
```

### Custom Agent Card

```python
from a2a.types import AgentCard

card = AgentCard(
    name="math_agent",
    url="http://localhost:8001",
    description="Solves math problems",
    version="1.0.0",
    capabilities={},
    skills=[{"id": "math", "name": "Math Solving"}],
)

a2a_app = to_a2a(root_agent, port=8001, agent_card=card)
```

## Consuming a Remote A2A Agent

```python
from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

remote_math = RemoteA2aAgent(
    name="math_agent",
    description="Agent that solves math problems.",
    agent_card="http://localhost:8001/.well-known/agent-card.json",
)

root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash",
    instruction="Delegate math questions to math_agent.",
    sub_agents=[remote_math],
)
```

## Complete Example

### Project Structure

```
a2a_demo/
├── remote_agent/
│   ├── __init__.py
│   └── agent.py         # Exposed via A2A (port 8001)
├── main_agent/
│   ├── __init__.py
│   └── agent.py         # Consumes remote agent
├── pyproject.toml
└── .env
```

### Remote Agent

```python
# remote_agent/agent.py
from google.adk.agents import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a

def check_prime(nums: list[int]) -> str:
    """Check if numbers are prime."""
    results = []
    for n in nums:
        if n < 2:
            results.append(f"{n} is not prime")
        elif all(n % i != 0 for i in range(2, int(n**0.5) + 1)):
            results.append(f"{n} is prime")
        else:
            results.append(f"{n} is not prime")
    return ", ".join(results)

root_agent = Agent(
    name="prime_checker",
    model="gemini-2.5-flash",
    instruction="Check if numbers are prime using the check_prime tool.",
    tools=[check_prime],
)

a2a_app = to_a2a(root_agent, port=8001)
```

### Main Agent

```python
# main_agent/agent.py
from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

prime_agent = RemoteA2aAgent(
    name="prime_checker",
    description="Checks if numbers are prime.",
    agent_card="http://localhost:8001/.well-known/agent-card.json",
)

root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash",
    instruction="Delegate prime checking to prime_checker.",
    sub_agents=[prime_agent],
)
```

### Running

```bash
# Terminal 1: Start remote A2A agent
uvicorn remote_agent.agent:a2a_app --host localhost --port 8001

# Terminal 2: Start main agent
adk web main_agent
```

## Testing A2A Agents

```python
import pytest
from google.adk.runners import InMemoryRunner
from google.genai import types
from main_agent.agent import root_agent

@pytest.mark.asyncio
async def test_a2a_prime_check():
    runner = InMemoryRunner(agent=root_agent, app_name="test")
    session = await runner.session_service.create_session(
        user_id="test_user", app_name="test"
    )
    content = types.Content(
        role="user",
        parts=[types.Part.from_text(text="Is 7 a prime number?")],
    )
    events = []
    async for event in runner.run_async(
        user_id="test_user", session_id=session.id, new_message=content
    ):
        events.append(event)
    
    assert "prime" in events[-1].content.parts[0].text.lower()
```

**Note:** Remote A2A server must be running before executing tests.

## Metadata Propagation

ADK propagates metadata across A2A boundaries:

```python
from google.adk.agents.run_config import RunConfig

run_config = RunConfig(
    custom_metadata={"trace_id": "abc-123", "user_tier": "premium"}
)

# Metadata appears in remote agent events as:
# event.custom_metadata["a2a_metadata"]["trace_id"]
```

## Port Configuration

| Agent | Default Port | Command |
|-------|-------------|---------|
| Main agent (`adk web`) | 8000 | `--port` |
| Remote A2A agent | 8001+ | `--port` or uvicorn `--port` |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused | Verify remote agent is running and port is correct |
| Agent card not found | Check `/.well-known/agent-card.json` endpoint |
| Import error on `to_a2a` | Install with `pip install google-adk[a2a]` |
| `Event loop is closed` | Run all A2A tests in a single `asyncio.run()` call |
| Timeout on A2A calls | Check network, increase timeout, verify agent card URL |
| Agent not routing to remote | Check `description` field -- it drives LLM routing |
