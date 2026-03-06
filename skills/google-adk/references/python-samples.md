---
name: adk-python-samples
version: "1.0.0"
description: Python code samples for Google ADK including basic agents, multi-agent pipelines, tool definitions, and deployment patterns.
metadata:
  source_url: https://github.com/google/adk-python
  docs_url: https://google.github.io/adk-docs/
---

# Python Samples

## Basic Agent

```python
# my_agent/__init__.py
from . import agent

# my_agent/agent.py
from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="basic_agent",
    model="gemini-2.5-flash",
    instruction="You are a helpful research assistant.",
    description="Basic search agent",
    tools=[google_search],
)
```

## Multi-Agent Pipeline

```python
from google.adk.agents import Agent, SequentialAgent, ParallelAgent

# Step 1: Research agents (parallel)
web_researcher = Agent(
    name="web_researcher",
    model="gemini-2.5-flash",
    instruction="Search the web for current information. Output key findings.",
    tools=[google_search],
    output_key="web_findings",
)

doc_researcher = Agent(
    name="doc_researcher",
    model="gemini-2.5-flash",
    instruction="Search internal documents. Output relevant sections.",
    output_key="doc_findings",
)

# Step 2: Synthesizer
synthesizer = Agent(
    name="synthesizer",
    model="gemini-2.5-flash",
    instruction="""Synthesize findings from web and document research.
    Web findings: {state[web_findings]}
    Document findings: {state[doc_findings]}
    
    Create a comprehensive summary.""",
    output_key="synthesis",
)

# Step 3: Writer
writer = Agent(
    name="writer",
    model="gemini-2.5-pro",
    instruction="""Write a report based on the synthesis:
    {state[synthesis]}
    
    Use professional tone. Include citations.""",
)

# Compose pipeline
research_pipeline = SequentialAgent(
    name="research_pipeline",
    sub_agents=[
        ParallelAgent(name="parallel_research", sub_agents=[web_researcher, doc_researcher]),
        synthesizer,
        writer,
    ],
)

root_agent = research_pipeline
```

## BigQuery with ADC

```python
from google.adk.agents import Agent
from google.adk.tools import ToolContext
from google.cloud import bigquery
from google.auth import default

def list_datasets(project_id: str, tool_context: ToolContext) -> dict:
    """List BigQuery datasets using ADC."""
    try:
        # ADC automatically finds credentials
        credentials, _ = default()
        client = bigquery.Client(project=project_id, credentials=credentials)
        
        datasets = list(client.list_datasets())
        return {
            "datasets": [
                {"id": ds.dataset_id, "project": ds.project}
                for ds in datasets
            ]
        }
    except Exception as e:
        return {"error": str(e)}

def query_bigquery(sql: str, project_id: str, tool_context: ToolContext) -> dict:
    """Execute BigQuery query with access control."""
    # Validate user permissions
    access_level = tool_context.state.get("user:access_level", "read_only")
    
    if access_level == "read_only":
        sql_upper = sql.strip().upper()
        if not sql_upper.startswith("SELECT") and not sql_upper.startswith("WITH"):
            return {"error": "Read-only users can only execute SELECT queries"}
    
    try:
        credentials, _ = default()
        client = bigquery.Client(project=project_id, credentials=credentials)
        
        query_job = client.query(sql)
        results = query_job.result()
        
        rows = [dict(row) for row in results]
        return {
            "rows": rows,
            "total_rows": len(rows),
            "columns": [field.name for field in query_job.result().schema]
        }
    except Exception as e:
        return {"error": str(e)}

root_agent = Agent(
    name="bq_agent",
    model="gemini-2.5-flash",
    instruction="Help users query BigQuery databases.",
    tools=[list_datasets, query_bigquery],
)
```

## WIF Authentication (Azure → GCP)

```python
from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import ToolContext
from google.auth import external_account
from google.auth.transport.requests import Request
from google.cloud import bigquery
import msal
import json

class AzureWIFAuth:
    """Azure to GCP Workload Identity Federation."""
    
    def __init__(self, project_id: str, pool_id: str, provider_id: str):
        self.project_id = project_id
        self.pool_id = pool_id
        self.provider_id = provider_id
        self.pool_resource = f"projects/{project_id}/locations/global/workloadIdentityPools/{pool_id}"
        self.provider_resource = f"{self.pool_resource}/providers/{provider_id}"
    
    def get_azure_token(self, tenant_id: str, client_id: str, client_secret: str = None) -> str:
        """Get Azure AD access token."""
        if client_secret:
            app = msal.ConfidentialClientApplication(
                client_id=client_id,
                client_credential=client_secret,
                authority=f"https://login.microsoftonline.com/{tenant_id}"
            )
            result = app.acquire_token_for_client(scopes=["https://management.azure.com/.default"])
        else:
            app = msal.PublicClientApplication(
                client_id=client_id,
                authority=f"https://login.microsoftonline.com/{tenant_id}"
            )
            result = app.acquire_token_interactive(scopes=["User.Read"])
        
        if "access_token" not in result:
            raise Exception(f"Failed to get Azure token: {result.get('error_description')}")
        
        return result["access_token"]
    
    def create_adc_config(self, azure_token: str, service_account_email: str) -> dict:
        """Create ADC-compatible credential configuration."""
        return {
            "type": "external_account",
            "audience": f"//iam.googleapis.com/{self.provider_resource}",
            "subject_token_type": "urn:ietf:params:oauth:token-type:jwt",
            "token_url": "https://sts.googleapis.com/v1/token",
            "service_account_impersonation_url": (
                f"https://iamcredentials.googleapis.com/v1/projects/-/"
                f"serviceAccounts/{service_account_email}:generateAccessToken"
            ),
            "credential_source": {
                "url": f"data:application/json;base64,",
                "format": {
                    "type": "json",
                    "subject_token_field_name": "token"
                }
            },
            "quota_project_id": self.project_id,
        }

def authenticate_with_azure(
    azure_tenant_id: str,
    azure_client_id: str,
    azure_client_secret: str = None,
    requested_role: str = "reader",
    tool_context: ToolContext
) -> dict:
    """Authenticate user via Azure WIF."""
    import os
    
    wif = AzureWIFAuth(
        project_id=os.getenv("GCP_PROJECT_ID"),
        pool_id=os.getenv("WIF_POOL_ID"),
        provider_id=os.getenv("WIF_PROVIDER_ID")
    )
    
    try:
        # Get Azure token
        azure_token = wif.get_azure_token(azure_tenant_id, azure_client_id, azure_client_secret)
        
        # Determine service account based on role
        if requested_role == "admin":
            sa_email = f"bq-admin@{os.getenv('GCP_PROJECT_ID')}.iam.gserviceaccount.com"
            tool_context.state["user:access_level"] = "admin"
        else:
            sa_email = f"bq-reader@{os.getenv('GCP_PROJECT_ID')}.iam.gserviceaccount.com"
            tool_context.state["user:access_level"] = "read_only"
        
        # Create ADC config
        config = wif.create_adc_config(azure_token, sa_email)
        
        # Store credentials using ADC
        credentials = external_account.Credentials.from_info(config)
        credentials.refresh(Request())
        
        tool_context.state["user:gcp_credentials"] = credentials
        tool_context.state["user:authenticated"] = True
        tool_context.state["user:service_account"] = sa_email
        
        return {
            "status": "authenticated",
            "service_account": sa_email,
            "access_level": tool_context.state["user:access_level"]
        }
    except Exception as e:
        return {"error": f"Authentication failed: {str(e)}"}

def query_with_wif(sql: str, project_id: str, tool_context: ToolContext) -> dict:
    """Query BigQuery using WIF-authenticated credentials."""
    credentials = tool_context.state.get("user:gcp_credentials")
    if not credentials:
        return {"error": "Not authenticated. Call authenticate_with_azure first."}
    
    # Refresh if needed
    if credentials.expired:
        credentials.refresh(Request())
        tool_context.state["user:gcp_credentials"] = credentials
    
    # Validate permissions
    access_level = tool_context.state.get("user:access_level", "read_only")
    if access_level == "read_only":
        sql_upper = sql.strip().upper()
        if not sql_upper.startswith("SELECT"):
            return {"error": "Read-only users can only execute SELECT queries"}
    
    try:
        client = bigquery.Client(project=project_id, credentials=credentials)
        results = client.query(sql).result()
        return {"rows": [dict(row) for row in results]}
    except Exception as e:
        return {"error": str(e)}

# Agent setup
auth_agent = Agent(
    name="auth_handler",
    model="gemini-2.5-flash",
    instruction="Authenticate users with Azure WIF before allowing BigQuery access.",
    tools=[authenticate_with_azure],
)

bq_agent = Agent(
    name="bq_query",
    model="gemini-2.5-flash",
    instruction="Execute BigQuery queries using authenticated WIF credentials.",
    tools=[query_with_wif],
)

root_agent = SequentialAgent(
    name="wif_bq_agent",
    sub_agents=[auth_agent, bq_agent],
)
```

## OAuth 2.0 (Google Calendar)

```python
from google.adk.agents import Agent
from google.adk.tools import ToolContext
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import json

# OAuth configuration
CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
REDIRECT_URI = "https://your-app.com/oauth/callback"

def get_authorization_url(tool_context: ToolContext) -> dict:
    """Get OAuth authorization URL for user consent."""
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )
    auth_url, state = flow.authorization_url(prompt="consent")
    
    # Store state for verification
    tool_context.state["oauth_state"] = state
    
    return {
        "status": "authorization_required",
        "authorization_url": auth_url,
        "instructions": "Please visit this URL and authorize access to your calendar."
    }

def exchange_auth_code(auth_code: str, tool_context: ToolContext) -> dict:
    """Exchange authorization code for access token."""
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )
    
    try:
        flow.fetch_token(code=auth_code)
        creds = flow.credentials
        
        # Store credentials in state
        tool_context.state["oauth_credentials"] = {
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": creds.scopes,
        }
        tool_context.state["user:calendar_authenticated"] = True
        
        return {"status": "authenticated", "scopes": creds.scopes}
    except Exception as e:
        return {"error": str(e)}

def list_calendar_events(
    max_results: int = 10,
    calendar_id: str = "primary",
    tool_context: ToolContext
) -> dict:
    """List calendar events using OAuth credentials."""
    creds_dict = tool_context.state.get("oauth_credentials")
    if not creds_dict:
        return {"error": "Not authenticated. Call get_authorization_url first."}
    
    # Reconstruct credentials
    creds = Credentials(**creds_dict)
    
    # Refresh if expired
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Update stored credentials
        tool_context.state["oauth_credentials"] = {
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": creds.scopes,
        }
    
    try:
        service = build("calendar", "v3", credentials=creds)
        events_result = service.events().list(
            calendarId=calendar_id,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        
        events = events_result.get("items", [])
        return {
            "events": [
                {
                    "id": event["id"],
                    "summary": event.get("summary", "No title"),
                    "start": event["start"],
                    "end": event["end"],
                }
                for event in events
            ]
        }
    except Exception as e:
        return {"error": str(e)}

root_agent = Agent(
    name="calendar_agent",
    model="gemini-2.5-flash",
    instruction="""Help users manage their Google Calendar.
    
    If not authenticated:
    1. Call get_authorization_url to get the authorization URL
    2. User visits URL and authorizes
    3. Call exchange_auth_code with the code
    
    Then use list_calendar_events to fetch calendar data.""",
    tools=[get_authorization_url, exchange_auth_code, list_calendar_events],
)
```

## MCP Toolset with Authentication

```python
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams
from mcp import StdioServerParameters
import os

# MCP server with auth
mcp_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-postgres"],
            env={
                "DATABASE_URL": os.getenv("DATABASE_URL"),
                "MCP_AUTH_TOKEN": os.getenv("MCP_AUTH_TOKEN"),
            },
        ),
    ),
)

root_agent = Agent(
    name="mcp_db_agent",
    model="gemini-2.5-flash",
    instruction="Query the database using MCP tools.",
    tools=[mcp_tools],
)
```

## Safety Guardrails

```python
from google.adk.agents import Agent
from google.genai import types
import re

# Safety settings
safety_settings = [
    types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_MEDIUM_AND_ABOVE"),
    types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_LOW_AND_ABOVE"),
]

# Input validation
def validate_input(callback_context, llm_request):
    """Block prompt injection attempts."""
    if not llm_request.contents:
        return None
    
    text = llm_request.contents[-1].parts[0].text.lower()
    
    injection_patterns = [
        r"ignore previous instructions",
        r"system prompt",
        r"you are now",
        r"jailbreak",
    ]
    
    for pattern in injection_patterns:
        if re.search(pattern, text):
            return types.Content(
                role="model",
                parts=[types.Part.from_text("I cannot process this request.")]
            )
    return None

# Tool authorization
def authorize_tool(tool, args, tool_context):
    """Validate user permissions before tool execution."""
    if tool.name in ["delete_data", "modify_data"]:
        role = tool_context.state.get("user:role")
        if role != "admin":
            return {"error": "Admin access required"}
    return None

root_agent = Agent(
    name="safe_agent",
    model="gemini-2.5-flash",
    instruction="You are a secure agent with safety guardrails.",
    generate_content_config=types.GenerateContentConfig(
        safety_settings=safety_settings,
    ),
    before_model_callback=validate_input,
    before_tool_callback=authorize_tool,
    tools=[safe_query_tool],
)
```

## Structured Output

```python
from google.adk.agents import Agent
from pydantic import BaseModel
from typing import List

class AnalysisResult(BaseModel):
    summary: str
    key_points: List[str]
    confidence: float
    recommendations: List[str]

root_agent = Agent(
    name="structured_agent",
    model="gemini-2.5-flash",
    instruction="Analyze the data and return structured results.",
    output_schema=AnalysisResult,
    output_key="analysis",
)
```

## Testing

```python
import pytest
from google.adk.runners import InMemoryRunner
from google.genai import types

@pytest.mark.asyncio
async def test_bq_agent():
    from agent import root_agent
    
    runner = InMemoryRunner(agent=root_agent, app_name="test")
    session = await runner.session_service.create_session(
        user_id="test_user", app_name="test"
    )
    
    content = types.Content(
        role="user",
        parts=[types.Part.from_text("List datasets in project my-project")],
    )
    
    events = []
    async for event in runner.run_async(
        user_id="test_user", session_id=session.id, new_message=content
    ):
        events.append(event)
    
    assert len(events) > 0
    response_text = events[-1].content.parts[0].text
    assert "dataset" in response_text.lower()
```

## Complete Project Structure

```
bigquery_agent/
├── bigquery_agent/
│   ├── __init__.py              # from . import agent
│   ├── agent.py                 # Root agent definition
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── bigquery.py          # BigQuery operations with ADC
│   │   └── auth.py              # WIF authentication
│   └── config/
│       └── wif.py               # WIF configuration
├── tests/
│   └── test_agent.py
├── pyproject.toml
└── .env.example                 # Template for env vars (no keys!)
```

## Environment Variables

```bash
# .env - Only non-sensitive configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1

# WIF Configuration (resource IDs, not credentials)
WIF_POOL_ID=azure-wif-pool
WIF_PROVIDER_ID=azure-provider

# OAuth (only client ID for consent URL generation)
OAUTH_CLIENT_ID=your-oauth-client-id
```
