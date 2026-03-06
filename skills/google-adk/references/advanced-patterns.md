---
name: adk-advanced-patterns
version: "1.0.0"
description: Advanced patterns for Google ADK including hierarchical workflows, parallel processing, deployment patterns, and custom runtimes.
metadata:
  source_url: https://google.github.io/adk-docs/
  docs_url: https://google.github.io/adk-docs/advanced
---

# Advanced Patterns

## Hierarchical Workflows

Nest agents for complex multi-step workflows:

```python
# Level 3: Leaf agents
email_drafter = Agent(name="email_drafter", output_key="email_draft", ...)
email_publisher = Agent(name="email_publisher", tools=[publish_email], ...)
slack_drafter = Agent(name="slack_drafter", output_key="slack_draft", ...)
slack_publisher = Agent(name="slack_publisher", tools=[post_to_slack], ...)

# Level 2: Channel pipelines
email_pipeline = SequentialAgent(sub_agents=[email_drafter, email_publisher])
slack_pipeline = SequentialAgent(sub_agents=[slack_drafter, slack_publisher])

# Level 1: Broadcast
broadcast = ParallelAgent(sub_agents=[email_pipeline, slack_pipeline])

# Root: Full workflow
root_agent = SequentialAgent(sub_agents=[message_enhancer, broadcast, summary_agent])
```

## Parallel Writers + Judge

Generate multiple candidates in parallel, select the best:

```python
from google.genai import types

creative_writer = Agent(
    name="creative",
    model="gemini-2.5-pro",
    generate_content_config=types.GenerateContentConfig(temperature=0.9),
    output_key="creative_candidate",
)

focused_writer = Agent(
    name="focused",
    model="gemini-2.5-pro",
    generate_content_config=types.GenerateContentConfig(temperature=0.2),
    output_key="focused_candidate",
)

judge = Agent(
    name="judge",
    instruction="Compare candidates and select the best.",
    output_key="final_selection",
)

root_agent = SequentialAgent(sub_agents=[
    ParallelAgent(sub_agents=[creative_writer, focused_writer]),
    judge,
])
```

## Agent Transfer (Sub-Agent Routing)

Let the LLM decide which sub-agent to delegate to:

```python
root_agent = Agent(
    name="router",
    instruction="""You are a customer service router.
    - For billing questions, transfer to billing_agent
    - For technical issues, transfer to tech_support_agent
    - For general inquiries, handle directly""",
    sub_agents=[billing_agent, tech_support_agent],
)
```

## Callback Patterns

### Rate Limiting

```python
import time

RPM_QUOTA = 15
RATE_LIMIT_SECS = 60

def rate_limit_callback(callback_context, llm_request):
    now = time.time()
    if "timer_start" not in callback_context.state:
        callback_context.state["timer_start"] = now
        callback_context.state["request_count"] = 1
        return

    count = callback_context.state["request_count"] + 1
    elapsed = now - callback_context.state["timer_start"]

    if count > RPM_QUOTA:
        delay = RATE_LIMIT_SECS - elapsed + 1
        if delay > 0:
            time.sleep(delay)
        callback_context.state["timer_start"] = now
        callback_context.state["request_count"] = 1
    else:
        callback_context.state["request_count"] = count
```

### Input Validation

```python
def validate_before_tool(tool, args, tool_context) -> dict | None:
    """Validate tool inputs, return dict to skip execution."""
    if "customer_id" in args:
        if not args["customer_id"].startswith("CUST-"):
            return {"error": "Invalid customer ID format. Expected CUST-XXXX."}

    if tool.name == "approve_discount" and args.get("value", 0) <= 10:
        return {"status": "auto_approved", "value": args["value"]}

    return None  # Proceed with execution
```

### State Initialization

```python
import uuid
from datetime import datetime

def init_session(callback_context):
    """Initialize session state before agent starts."""
    callback_context.state.setdefault("session_id", str(uuid.uuid4()))
    callback_context.state.setdefault("started_at", datetime.now().isoformat())
    callback_context.state.setdefault("turn_count", 0)
    callback_context.state["turn_count"] += 1
```

## Safety and Guardrails

### Before-Model Guardrail

```python
def content_safety_check(callback_context, llm_request):
    """Block unsafe requests before they reach the model."""
    if not llm_request.contents:
        return None

    last_msg = llm_request.contents[-1]
    if last_msg.role == "user":
        text = last_msg.parts[0].text if last_msg.parts else ""
        if is_unsafe(text):
            return types.Content(
                role="model",
                parts=[types.Part.from_text("I cannot process this request.")],
            )
    return None
```

## Deployment

### Local Development

```bash
adk run my_agent          # Interactive terminal
adk web my_agent          # Web UI on localhost
```

### Cloud Run

```bash
adk deploy cloud_run \
    --project=my-project \
    --region=us-central1 \
    --service_name=my-agent \
    my_agent
```

### FastAPI Integration

```python
from fastapi import FastAPI
from google.adk.runners import InMemoryRunner

app = FastAPI()
runner = InMemoryRunner(agent=root_agent, app_name="api")

@app.post("/chat")
async def chat(message: str, session_id: str):
    content = types.Content(role="user", parts=[types.Part.from_text(text=message)])
    events = []
    async for event in runner.run_async(
        user_id="api_user", session_id=session_id, new_message=content,
    ):
        events.append(event)
    return {"response": events[-1].content.parts[0].text}
```

## Project Configuration

### pyproject.toml

```toml
[project]
name = "my-agent"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = ["google-adk"]

[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"
```

### Environment-Based Config

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="AGENT_")
    model: str = "gemini-2.5-flash"
    temperature: float = 0.7
    google_api_key: str = ""

config = Config()

root_agent = Agent(
    model=config.model,
    generate_content_config=types.GenerateContentConfig(temperature=config.temperature),
)
```

### .env File

```bash
GOOGLE_API_KEY=your-api-key
# OR for Vertex AI:
GOOGLE_CLOUD_PROJECT=my-project
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

## Anti-Patterns to Avoid

1. **Don't use global variables for state** - Use `tool_context.state`
2. **Don't create monolithic agents** - Split into focused sub-agents
3. **Don't skip `__init__.py`** - ADK won't find your agent
4. **Don't hardcode API keys** - Use `.env` files
5. **Don't ignore structured output** - Use `output_schema`
6. **Don't nest references too deep** - Max 3-4 levels
7. **Don't forget `root_agent`** - Must be module-level
8. **Don't use Agent when SequentialAgent is needed**
9. **Don't put all prompts inline** - Extract to `prompts.py`
10. **Don't skip testing** - Use `InMemoryRunner`
