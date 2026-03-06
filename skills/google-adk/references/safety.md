---
name: adk-safety
version: "1.0.0"
description: Safety and security patterns for Google ADK including input validation, output filtering, tool guards, content safety, and audit logging.
metadata:
  source_url: https://google.github.io/adk-docs/
  docs_url: https://google.github.io/adk-docs/safety
---

# Safety & Security

## Overview

ADK provides layered safety mechanisms for building secure agents:

| Layer | Mechanism | Purpose |
|-------|-----------|---------|
| Input Validation | `before_model_callback` | Block prompt injection, jailbreaks |
| Output Filtering | `after_model_callback` | Catch toxicity, policy violations |
| Tool Guards | `before_tool_callback` | Prevent unauthorized actions |
| Content Safety | Model Armor / Safety filters | Built-in harm prevention |
| Identity & Access | WIF, OAuth, IAM | Authentication & authorization |
| Audit Logging | Custom callbacks | Compliance & forensics |

## Layered Defense Architecture

```
User Input
    ↓
┌─────────────────────────────────────┐
│  Layer 1: Input Validation          │  before_model_callback
│  - Prompt injection detection       │
│  - Jailbreak prevention             │
│  - Content policy checks            │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Layer 2: Model Safety              │  Model Armor / Safety settings
│  - Harmful content filtering        │
│  - Toxicity detection               │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Layer 3: Tool Guards               │  before_tool_callback
│  - Parameter validation             │
│  - Rate limiting                    │
│  - Authorization checks             │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Layer 4: Output Filtering          │  after_model_callback
│  - PII redaction                    │
│  - Policy violation detection       │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Layer 5: Audit & Monitoring        │  Custom logging
│  - Action logging                   │
│  - Anomaly detection                │
└─────────────────────────────────────┘
```

## Input Validation

### Prompt Injection Detection

```python
from google.adk.agents import Agent
from google.genai import types
import re

PROMPT_INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"disregard (your|the) (prompt|instructions)",
    r"system prompt",
    r"you are now",
    r"DAN (do anything now)",
    r"jailbreak",
    r"\[system\]",
    r"\[instructions\]",
]

def detect_prompt_injection(text: str) -> tuple[bool, str]:
    """Detect common prompt injection attempts."""
    text_lower = text.lower()
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, text_lower):
            return True, f"Detected pattern: {pattern}"
    return False, ""

def input_validation_callback(callback_context, llm_request):
    """Validate user input before sending to model."""
    if not llm_request.contents:
        return None
    
    last_content = llm_request.contents[-1]
    if last_content.role == "user":
        text = last_content.parts[0].text if last_content.parts else ""
        
        is_injection, reason = detect_prompt_injection(text)
        if is_injection:
            # Log the attempt
            print(f"SECURITY: Prompt injection detected - {reason}")
            
            # Return safe response instead of processing
            return types.Content(
                role="model",
                parts=[types.Part.from_text(
                    "I cannot process this request. Please rephrase without attempting to modify my instructions."
                )]
            )
    
    return None  # Proceed normally

agent = Agent(
    name="guarded_agent",
    model="gemini-2.5-flash",
    before_model_callback=input_validation_callback,
)
```

### Content Policy Enforcement

```python
import re
from typing import Optional

class ContentPolicy:
    """Define content policies for the agent."""
    
    PROHIBITED_TOPICS = [
        "harmful_instructions",
        "illegal_activities", 
        "personal_data_extraction",
        "competitor_intelligence",
    ]
    
    @classmethod
    def validate(cls, text: str) -> tuple[bool, Optional[str]]:
        """Validate content against policies."""
        # Check for PII extraction attempts
        pii_patterns = [
            r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
            r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",  # Credit card
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
        ]
        
        for pattern in pii_patterns:
            if re.search(pattern, text):
                return False, "Content appears to request or contain PII"
        
        return True, None

def policy_enforcement_callback(callback_context, llm_request):
    """Enforce content policies on input."""
    if not llm_request.contents:
        return None
    
    text = llm_request.contents[-1].parts[0].text
    is_valid, reason = ContentPolicy.validate(text)
    
    if not is_valid:
        return types.Content(
            role="model",
            parts=[types.Part.from_text(f"I cannot fulfill this request. {reason}")]
        )
    
    return None
```

## Model Safety Settings

### Safety Filter Configuration

```python
from google.genai import types
from google.adk.agents import Agent

safety_settings = [
    types.SafetySetting(
        category="HARM_CATEGORY_HARASSMENT",
        threshold="BLOCK_MEDIUM_AND_ABOVE"
    ),
    types.SafetySetting(
        category="HARM_CATEGORY_HATE_SPEECH",
        threshold="BLOCK_LOW_AND_ABOVE"
    ),
    types.SafetySetting(
        category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
        threshold="BLOCK_MEDIUM_AND_ABOVE"
    ),
    types.SafetySetting(
        category="HARM_CATEGORY_DANGEROUS_CONTENT",
        threshold="BLOCK_LOW_AND_ABOVE"
    ),
]

agent = Agent(
    name="safe_agent",
    model="gemini-2.5-flash",
    generate_content_config=types.GenerateContentConfig(
        safety_settings=safety_settings,
    ),
)
```

## Tool Guards

### Authorization Checks

```python
from google.adk.tools import ToolContext

def before_tool_callback(tool, args, tool_context) -> dict | None:
    """Validate tool execution authorization."""
    
    # Check user authentication
    if not tool_context.state.get("user:authenticated"):
        return {"error": "Authentication required"}
    
    # Tool-specific authorization
    if tool.name == "delete_database":
        role = tool_context.state.get("user:role")
        if role != "admin":
            return {"error": "Admin role required for database deletion"}
    
    if tool.name == "approve_purchase":
        amount = args.get("amount", 0)
        approval_limit = tool_context.state.get("user:approval_limit", 0)
        if amount > approval_limit:
            return {
                "error": f"Amount ${amount} exceeds approval limit of ${approval_limit}",
                "requires_escalation": True
            }
    
    if tool.name == "access_sensitive_data":
        # Check if user has explicit consent
        if not tool_context.state.get("user:data_access_consent"):
            return {"error": "User consent required for accessing sensitive data"}
    
    return None  # Proceed with tool execution

agent = Agent(
    name="guarded_agent",
    tools=[delete_database, approve_purchase, access_sensitive_data],
    before_tool_callback=before_tool_callback,
)
```

### Rate Limiting

```python
import time
from collections import defaultdict

class RateLimiter:
    """Simple rate limiter for tool calls."""
    
    def __init__(self, max_calls: int = 10, window_seconds: int = 60):
        self.max_calls = max_calls
        self.window = window_seconds
        self.calls = defaultdict(list)
    
    def is_allowed(self, user_id: str) -> bool:
        """Check if user is within rate limit."""
        now = time.time()
        user_calls = self.calls[user_id]
        
        # Remove old calls outside the window
        self.calls[user_id] = [t for t in user_calls if now - t < self.window]
        
        return len(self.calls[user_id]) < self.max_calls
    
    def record_call(self, user_id: str):
        """Record a tool call."""
        self.calls[user_id].append(time.time())

rate_limiter = RateLimiter(max_calls=10, window_seconds=60)

def rate_limited_before_tool(tool, args, tool_context):
    """Apply rate limiting to tool calls."""
    user_id = tool_context.state.get("user:id", "anonymous")
    
    if not rate_limiter.is_allowed(user_id):
        return {
            "error": "Rate limit exceeded. Please wait before making more requests."
        }
    
    rate_limiter.record_call(user_id)
    return None
```

### Parameter Validation

```python
from typing import Any
import re

class ParameterValidator:
    """Validate tool parameters."""
    
    @staticmethod
    def validate_sql(sql: str) -> tuple[bool, str]:
        """Validate SQL query for injection attempts."""
        dangerous_patterns = [
            r";\s*drop\s+",
            r";\s*delete\s+",
            r";\s*update\s+.*\s+set\s+",
            r"union\s+select",
            r"--",
            r"/\*",
        ]
        
        sql_lower = sql.lower()
        for pattern in dangerous_patterns:
            if re.search(pattern, sql_lower):
                return False, f"Potentially dangerous SQL pattern detected"
        
        return True, ""
    
    @staticmethod
    def validate_email(email: str) -> tuple[bool, str]:
        """Validate email format."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, email):
            return False, "Invalid email format"
        return True, ""

def validate_tool_parameters(tool, args: dict) -> dict | None:
    """Validate tool parameters before execution."""
    
    if tool.name == "execute_sql":
        sql = args.get("sql", "")
        is_valid, error = ParameterValidator.validate_sql(sql)
        if not is_valid:
            return {"error": f"SQL validation failed: {error}"}
    
    if tool.name == "send_email":
        email = args.get("to_email", "")
        is_valid, error = ParameterValidator.validate_email(email)
        if not is_valid:
            return {"error": f"Email validation failed: {error}"}
    
    return None
```

## Output Filtering

### PII Redaction

```python
import re
from google.adk.agents import Agent
from google.genai import types

PII_PATTERNS = {
    "ssn": (r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]"),
    "credit_card": (r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b", "[REDACTED-CC]"),
    "email": (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[REDACTED-EMAIL]"),
    "phone": (r"\b\d{3}[\s.-]?\d{3}[\s.-]?\d{4}\b", "[REDACTED-PHONE]"),
}

def redact_pii(text: str) -> str:
    """Redact PII from text."""
    for pii_type, (pattern, replacement) in PII_PATTERNS.items():
        text = re.sub(pattern, replacement, text)
    return text

def output_filter_callback(callback_context, llm_response):
    """Filter model output for PII."""
    if not llm_response.content or not llm_response.content.parts:
        return llm_response
    
    # Redact PII from each text part
    for part in llm_response.content.parts:
        if hasattr(part, 'text') and part.text:
            part.text = redact_pii(part.text)
    
    return llm_response

agent = Agent(
    name="pii_safe_agent",
    model="gemini-2.5-flash",
    after_model_callback=output_filter_callback,
)
```

### Content Moderation

```python
def moderate_output(callback_context, llm_response):
    """Moderate model output for policy violations."""
    if not llm_response.content or not llm_response.content.parts:
        return llm_response
    
    text = llm_response.content.parts[0].text.lower()
    
    # Check for policy violations
    violations = []
    
    if any(word in text for word in ["confidential", "proprietary", "internal only"]):
        if not callback_context.state.get("user:internal_access"):
            violations.append("Potential disclosure of internal information")
    
    if violations:
        # Replace content with warning
        return types.Content(
            role="model",
            parts=[types.Part.from_text(
                "I cannot provide this response as it may contain sensitive information."
            )]
        )
    
    return llm_response
```

## Audit Logging

### Security Event Logging

```python
import json
import logging
from datetime import datetime
from enum import Enum

class SecurityEventType(Enum):
    AUTH_SUCCESS = "auth_success"
    AUTH_FAILURE = "auth_failure"
    TOOL_ACCESS = "tool_access"
    POLICY_VIOLATION = "policy_violation"
    RATE_LIMIT_HIT = "rate_limit_hit"
    SENSITIVE_DATA_ACCESS = "sensitive_data_access"

class SecurityAuditLogger:
    """Audit logger for security events."""
    
    def __init__(self):
        self.logger = logging.getLogger("adk.security")
        self.logger.setLevel(logging.INFO)
    
    def log_event(
        self,
        event_type: SecurityEventType,
        user_id: str,
        details: dict,
        tool_context=None
    ):
        """Log a security event."""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type.value,
            "user_id": user_id,
            "session_id": tool_context.state.get("session_id") if tool_context else None,
            "details": details,
        }
        
        self.logger.info(json.dumps(event))
        
        # Also store in state for session tracking
        if tool_context:
            if "security_events" not in tool_context.state:
                tool_context.state["security_events"] = []
            tool_context.state["security_events"].append(event)

audit_logger = SecurityAuditLogger()

# Usage in callbacks
def before_tool_with_audit(tool, args, tool_context):
    """Log tool access attempts."""
    user_id = tool_context.state.get("user:id", "anonymous")
    
    audit_logger.log_event(
        event_type=SecurityEventType.TOOL_ACCESS,
        user_id=user_id,
        details={
            "tool": tool.name,
            "args": {k: v for k, v in args.items() if k not in ["password", "token", "secret"]},
        },
        tool_context=tool_context
    )
    
    return None  # Proceed with tool
```

## Complete Security Agent Example

```python
from google.adk.agents import Agent
from google.genai import types

# Security configuration
class SecurityConfig:
    """Security configuration for agents."""
    
    SAFETY_SETTINGS = [
        types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_MEDIUM_AND_ABOVE"),
        types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_LOW_AND_ABOVE"),
        types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_LOW_AND_ABOVE"),
    ]
    
    RATE_LIMIT = {"max_calls": 50, "window_seconds": 3600}  # 50 calls per hour

# Combined security callbacks
def security_input_guard(callback_context, llm_request):
    """Combined input validation."""
    if not llm_request.contents:
        return None
    
    text = llm_request.contents[-1].parts[0].text
    user_id = callback_context.state.get("user:id", "anonymous")
    
    # Check prompt injection
    is_injection, reason = detect_prompt_injection(text)
    if is_injection:
        audit_logger.log_event(
            SecurityEventType.POLICY_VIOLATION,
            user_id,
            {"violation": "prompt_injection", "reason": reason}
        )
        return types.Content(
            role="model",
            parts=[types.Part.from_text("Request blocked for security reasons.")]
        )
    
    # Check content policy
    is_valid, reason = ContentPolicy.validate(text)
    if not is_valid:
        return types.Content(
            role="model",
            parts=[types.Part.from_text(f"Cannot process: {reason}")]
        )
    
    return None

def security_tool_guard(tool, args, tool_context):
    """Combined tool security."""
    user_id = tool_context.state.get("user:id", "anonymous")
    
    # Rate limiting
    if not rate_limiter.is_allowed(user_id):
        audit_logger.log_event(
            SecurityEventType.RATE_LIMIT_HIT,
            user_id,
            {"tool": tool.name}
        )
        return {"error": "Rate limit exceeded"}
    
    rate_limiter.record_call(user_id)
    
    # Authorization
    if not tool_context.state.get("user:authenticated"):
        return {"error": "Authentication required"}
    
    # Parameter validation
    result = validate_tool_parameters(tool, args)
    if result:
        return result
    
    # Audit logging
    audit_logger.log_event(
        SecurityEventType.TOOL_ACCESS,
        user_id,
        {"tool": tool.name, "args_keys": list(args.keys())},
        tool_context
    )
    
    return None

def security_output_filter(callback_context, llm_response):
    """Combined output filtering."""
    if not llm_response.content or not llm_response.content.parts:
        return llm_response
    
    # Redact PII
    for part in llm_response.content.parts:
        if hasattr(part, 'text'):
            part.text = redact_pii(part.text)
    
    return llm_response

# Secure agent
secure_agent = Agent(
    name="secure_agent",
    model="gemini-2.5-flash",
    instruction="You are a secure agent with safety guardrails.",
    generate_content_config=types.GenerateContentConfig(
        safety_settings=SecurityConfig.SAFETY_SETTINGS,
    ),
    before_model_callback=security_input_guard,
    before_tool_callback=security_tool_guard,
    after_model_callback=security_output_filter,
    tools=[safe_tool_1, safe_tool_2],
)
```

## Model Armor Integration

```python
# For enterprise-grade safety, use Google Cloud Model Armor
from google.cloud import modelarmor_v1

class ModelArmorGuard:
    """Integration with Google Cloud Model Armor."""
    
    def __init__(self, project_id: str, location: str = "us-central1"):
        self.client = modelarmor_v1.ModelArmorClient()
        self.template_name = f"projects/{project_id}/locations/{location}/templates/default"
    
    def sanitize_content(self, content: str) -> tuple[bool, str]:
        """Sanitize content using Model Armor."""
        request = modelarmor_v1.SanitizeUserPromptRequest(
            parent=self.template_name,
            user_prompt_content=modelarmor_v1.DataItem(
                text_data=modelarmor_v1.TextData(text=content)
            )
        )
        
        response = self.client.sanitize_user_prompt(request)
        
        if response.filter_match_state == modelarmor_v1.FilterMatchState.MATCH_FOUND:
            return False, "Content violates safety policies"
        
        return True, response.sanitized_user_prompt_content.text_data.text

# Use in callback
model_armor = ModelArmorGuard(project_id="my-project")

def model_armor_guard(callback_context, llm_request):
    """Use Model Armor for content filtering."""
    text = llm_request.contents[-1].parts[0].text
    
    is_safe, result = model_armor.sanitize_content(text)
    if not is_safe:
        return types.Content(role="model", parts=[types.Part.from_text(result)])
    
    # Update request with sanitized content
    llm_request.contents[-1].parts[0].text = result
    return None
```

## Best Practices

1. **Defense in Depth** - Never rely on a single security mechanism
2. **Fail Secure** - Default to blocking if validation is unclear
3. **Audit Everything** - Log all security-relevant events
4. **Rate Limit** - Prevent abuse and DoS attacks
5. **Validate Early** - Check input before model processing
6. **Filter Output** - Redact PII and sensitive data
7. **Least Privilege** - Tools should only access necessary data
8. **Monitor & Alert** - Set up alerts for security events

## Troubleshooting

| Issue | Solution |
|-------|----------|
| False positives in filtering | Adjust sensitivity thresholds |
| Bypass attempts detected | Review and update detection patterns |
| Performance impact | Cache validation results, use async checks |
| Compliance requirements | Enable full audit logging |
