---
name: adk-evaluation
version: "1.0.0"
description: Evaluation and testing patterns for Google ADK including eval data formats, metrics, session-based testing, and CI/CD integration.
metadata:
  source_url: https://google.github.io/adk-docs/
  docs_url: https://google.github.io/adk-docs/evaluation
---

# Evaluation & Testing

## Why Evaluate

- **Tool correctness** - Did the agent call right tools with right arguments?
- **Response quality** - Is the final answer accurate and complete?
- **Safety** - Does the agent avoid harmful content?
- **Groundedness** - Are claims supported by context?
- **Regression** - Do updates preserve existing behavior?

## Eval Data Format

ADK uses Pydantic-backed schemas. Files use `.test.json` (unit tests) or `.evalset.json` (integration tests).

### Single-Turn Eval Case

```json
{
  "eval_set_id": "weather_tests",
  "eval_cases": [{
    "eval_id": "turn_off_device",
    "conversation": [{
      "invocation_id": "inv-001",
      "user_content": {"parts": [{"text": "Turn off device_2 in Bedroom"}], "role": "user"},
      "final_response": {"parts": [{"text": "Device turned off"}], "role": "model"},
      "intermediate_data": {
        "tool_uses": [{"name": "set_device", "args": {"location": "Bedroom", "device_id": "device_2", "status": "OFF"}}]
      }
    }],
    "session_input": {"app_name": "home_agent", "user_id": "test", "state": {}}
  }]
}
```

### Multi-Turn Eval Case

```json
{
  "eval_id": "multi_turn",
  "conversation": [
    {
      "invocation_id": "inv-001",
      "user_content": {"parts": [{"text": "Roll a 10-sided die twice"}], "role": "user"},
      "final_response": {"parts": [{"text": "Rolled 4 and 7"}], "role": "model"},
      "intermediate_data": {"tool_uses": [{"name": "roll_die", "args": {"sides": 10}}, {"name": "roll_die", "args": {"sides": 10}}]}
    },
    {
      "invocation_id": "inv-002",
      "user_content": {"parts": [{"text": "Check if 9 is prime"}], "role": "user"},
      "final_response": {"parts": [{"text": "9 is not prime"}], "role": "model"},
      "intermediate_data": {"tool_uses": [{"name": "check_prime", "args": {"nums": [9]}}]}
    }
  ]
}
```

## Evaluation Criteria

| Criterion | Type | Reference-Based |
|-----------|------|-----------------|
| `tool_trajectory_avg_score` | Tool trajectory match | Yes |
| `response_match_score` | ROUGE-1 text overlap | Yes |
| `final_response_match_v2` | Semantic match (LLM judge) | Yes |
| `rubric_based_final_response_quality_v1` | Response quality rubrics | No |
| `rubric_based_tool_use_quality_v1` | Tool use quality rubrics | No |
| `hallucinations_v1` | Groundedness check | No |
| `safety_v1` | Harmlessness check | No |

**Defaults**: `tool_trajectory_avg_score: 1.0`, `response_match_score: 0.8`

### Tool Trajectory Evaluation

| Match Type | Behavior |
|------------|----------|
| `EXACT` | Same tools, args, order, no extras |
| `IN_ORDER` | Expected tools appear in order, other calls allowed between |
| `ANY_ORDER` | Expected tools all appear, order doesn't matter |

```json
{
  "criteria": {
    "tool_trajectory_avg_score": {"threshold": 1.0, "match_type": "EXACT"}
  }
}
```

### Semantic Response Match (LLM Judge)

```json
{
  "criteria": {
    "final_response_match_v2": {
      "threshold": 0.8,
      "judge_model_options": {"judge_model": "gemini-2.5-flash", "num_samples": 5}
    }
  }
}
```

### Rubric-Based Quality

```json
{
  "criteria": {
    "rubric_based_final_response_quality_v1": {
      "threshold": 0.8,
      "judge_model_options": {"judge_model": "gemini-2.5-flash", "num_samples": 5},
      "rubrics": [
        {"rubric_id": "conciseness", "rubric_content": {"text_property": "Response is direct and to the point"}},
        {"rubric_id": "accuracy", "rubric_content": {"text_property": "Information is factually correct"}}
      ]
    }
  }
}
```

### Hallucination Detection

```json
{
  "criteria": {
    "hallucinations_v1": {
      "threshold": 0.8,
      "judge_model_options": {"judge_model": "gemini-2.5-flash"},
      "evaluate_intermediate_nl_responses": true
    }
  }
}
```

## Running Evaluations

### CLI (`adk eval`)

```bash
# Basic
adk eval my_agent my_agent/eval_set.evalset.json

# With config
adk eval my_agent my_agent/eval_set.evalset.json --config_file_path my_agent/test_config.json --print_detailed_results

# Specific cases
adk eval my_agent my_agent/eval_set.evalset.json:case_1,case_2
```

### Pytest (`AgentEvaluator`)

```python
from google.adk.evaluation.agent_evaluator import AgentEvaluator
import pytest

@pytest.mark.asyncio
async def test_basic_tool_use():
    await AgentEvaluator.evaluate(
        agent_module="my_agent",
        eval_dataset_file_path_or_dir="tests/eval/basic.test.json",
    )

@pytest.mark.asyncio
async def test_eval_directory():
    await AgentEvaluator.evaluate(
        agent_module="my_agent",
        eval_dataset_file_path_or_dir="tests/eval/",
    )
```

### Web UI

```bash
adk web my_agent
```

1. Interact with agent to create session
2. Navigate to **Eval** tab
3. Click **Add current session** to create eval case
4. Edit cases as needed
5. Click **Run Evaluation** with metric thresholds

## User Simulation

For conversational agents, use `ConversationScenario` to dynamically generate user prompts:

```json
{
  "scenarios": [
    {
      "starting_prompt": "What can you do?",
      "conversation_plan": "Ask to roll a 20-sided die, then ask if the result is prime"
    }
  ]
}
```

```bash
adk eval_set create my_agent my_eval_set
adk eval_set add_eval_case my_agent my_eval_set --scenarios_file my_agent/scenarios.json
```

## Test Config File

```json
{
  "criteria": {
    "tool_trajectory_avg_score": {"threshold": 1.0, "match_type": "IN_ORDER"},
    "response_match_score": 0.8,
    "hallucinations_v1": {"threshold": 0.8, "evaluate_intermediate_nl_responses": true},
    "safety_v1": 0.8
  },
  "user_simulator_config": {
    "model": "gemini-2.5-flash",
    "max_allowed_invocations": 20
  }
}
```

## Unit Testing with InMemoryRunner

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
    content = types.Content(
        role="user",
        parts=[types.Part.from_text(text="Hello")],
    )
    events = []
    async for event in runner.run_async(
        user_id="test_user", session_id=session.id, new_message=content
    ):
        events.append(event)
    
    final_text = events[-1].content.parts[0].text
    assert "expected" in final_text.lower()
```

## Best Practices

1. **Start with tool trajectory** - Most bugs manifest as wrong tool calls
2. **Isolate tool calls** - One eval case per pattern
3. **Cover edge cases** - Empty inputs, missing params, errors
4. **Use rubrics for subjective quality** - When "correct" has multiple forms
5. **Layer metrics** - Combine fast deterministic with deeper quality checks
6. **Keep `.test.json` for unit tests** - Fast, single-session
7. **Use `.evalset.json` for integration** - Multi-session, complex flows
8. **Use web UI to bootstrap** - Interact, save, edit eval cases
9. **Add config to source control** - Reproducibility
10. **Run user simulation for conversational agents**
