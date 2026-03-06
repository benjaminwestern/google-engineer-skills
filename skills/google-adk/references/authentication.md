---
name: adk-authentication
version: "1.0.0"
description: Authentication and authorization for Google ADK including ADC (Application Default Credentials), Workload Identity Federation, and OAuth 2.0 patterns.
metadata:
  source_url: https://cloud.google.com/docs/authentication
  docs_url: https://google.github.io/adk-docs/authentication
---

# Authentication & Authorization

## Overview

ADK uses **Application Default Credentials (ADC)** as the primary authentication method. ADC automatically discovers credentials in GCP environments (Agent Engine, Cloud Run, GKE) without any configuration.

| Method | Use Case | Priority |
|--------|----------|----------|
| **Application Default Credentials (ADC)** | GCP-native workloads | **PRIMARY** |
| **Workload Identity Federation** | Azure/AWS → GCP | For multi-cloud |
| **OAuth 2.0** | User-facing apps (Calendar, Gmail) | For user auth |
| **GOOGLE_API_KEY** | Local prototyping only | Development only |
| **Service Account Keys** | **AVOID** - Use ADC instead | Legacy only |

## Application Default Credentials (ADC)

### How ADC Works

ADC automatically finds credentials from the environment in this order:

1. **GOOGLE_APPLICATION_CREDENTIALS** environment variable (file path) - Development only
2. **Default service account** - When running on GCP (Cloud Run, GKE, Agent Engine, Compute Engine)
3. **gcloud CLI credentials** - Local development via `gcloud auth application-default login`

### Local Development

```bash
# Authenticate locally (creates ~/.config/gcloud/application_default_credentials.json)
gcloud auth application-default login

# Set quota project for billing
gcloud auth application-default set-quota-project PROJECT_ID
```

### Production (Agent Engine, Cloud Run, GKE)

**No code changes needed.** ADC automatically uses the service account attached to the compute resource.

```python
# Works everywhere - local dev AND production
from google.cloud import bigquery
from google.auth import default

# ADC automatically finds credentials
credentials, project = default()

# Or even simpler - Client uses ADC by default
client = bigquery.Client(project=project_id)  # Uses ADC automatically
```

### Attaching Service Accounts

**Cloud Run:**
```bash
gcloud run deploy my-agent \
  --service-account=my-agent-sa@project.iam.gserviceaccount.com \
  --region=us-central1
```

**Agent Engine:**
```python
from google.adk.deployment import AgentEngine

agent = AgentEngine(
    agent=root_agent,
    service_account="my-agent-sa@project.iam.gserviceaccount.com",
)
```

**GKE Workload Identity:**
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-agent-sa
  annotations:
    iam.gke.io/gcp-service-account: my-agent-sa@project.iam.gserviceaccount.com
```

## Workload Identity Federation (Azure → GCP)

### Architecture

Use WIF when your users are in Azure but need to access GCP resources. ADC supports WIF natively.

```
Azure User/Service Principal
    ↓
Azure Entra ID Token
    ↓
GCP Workload Identity Pool Provider
    ↓
Service Account Impersonation (via ADC)
    ↓
BigQuery / GCP Resources
```

### Setup

**1. Create Workload Identity Pool**

```bash
export PROJECT_ID="your-project"
export POOL_NAME="azure-wif-pool"

# Create pool
gcloud iam workload-identity-pools create $POOL_NAME \
    --project=$PROJECT_ID --location="global"

export POOL_ID=$(gcloud iam workload-identity-pools describe $POOL_NAME \
    --project=$PROJECT_ID --location="global" --format='value(name)')
```

**2. Create Workload Identity Provider**

```bash
gcloud iam workload-identity-pools providers create-oidc azure-provider \
    --project=$PROJECT_ID --location="global" \
    --workload-identity-pool=$POOL_NAME \
    --attribute-mapping="google.subject=assertion.sub,google.groups=assertion.groups" \
    --attribute-condition="assertion.tid=='YOUR-AZURE-TENANT-ID'" \
    --issuer-uri="https://login.microsoftonline.com/YOUR-AZURE-TENANT-ID/v2.0"
```

**3. Create Service Accounts with Attribute-Based Access**

```bash
# Reader service account
gcloud iam service-accounts create bq-reader \
    --display-name="BigQuery Reader"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:bq-reader@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataViewer"

# Grant WIF access based on Azure AD group
gcloud iam service-accounts add-iam-policy-binding \
    bq-reader@$PROJECT_ID.iam.gserviceaccount.com \
    --role="roles/iam.workloadIdentityUser" \
    --member="principalSet://iam.googleapis.com/$POOL_ID/group/bigquery-readers"

# Admin service account for elevated access
gcloud iam service-accounts create bq-admin
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:bq-admin@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataEditor"
gcloud iam service-accounts add-iam-policy-binding \
    bq-admin@$PROJECT_ID.iam.gserviceaccount.com \
    --role="roles/iam.workloadIdentityUser" \
    --member="principalSet://iam.googleapis.com/$POOL_ID/group/bigquery-admins"
```

### ADC with WIF in ADK

```python
# config/wif_config.py
import json
import os

def create_wif_credential_config(
    project_id: str,
    pool_id: str,
    provider_id: str,
    service_account_email: str,
    azure_tenant_id: str,
    azure_client_id: str,
) -> dict:
    """Create ADC-compatible credential configuration for WIF.
    
    This config file is used by ADC automatically - no code changes needed.
    """
    pool_name = f"projects/{project_id}/locations/global/workloadIdentityPools/{pool_id}"
    provider_name = f"{pool_name}/providers/{provider_id}"
    
    return {
        "type": "external_account",
        "audience": f"//iam.googleapis.com/{provider_name}",
        "subject_token_type": "urn:ietf:params:oauth:token-type:jwt",
        "token_url": "https://sts.googleapis.com/v1/token",
        "service_account_impersonation_url": (
            f"https://iamcredentials.googleapis.com/v1/projects/-/"
            f"serviceAccounts/{service_account_email}:generateAccessToken"
        ),
        "credential_source": {
            "url": f"https://login.microsoftonline.com/{azure_tenant_id}/oauth2/v2.0/token",
            "headers": {"client_id": azure_client_id},
            "method": "POST",
            "format": {
                "type": "json",
                "subject_token_field_name": "access_token"
            }
        },
    }

# Save config for ADC to use
config = create_wif_credential_config(
    project_id="my-project",
    pool_id="azure-wif-pool",
    provider_id="azure-provider",
    service_account_email="bq-reader@my-project.iam.gserviceaccount.com",
    azure_tenant_id="your-tenant-id",
    azure_client_id="your-client-id",
)

# Write to file that ADC will find
# In production, this is mounted as a secret or config map
with open("/etc/gcp/wif-config.json", "w") as f:
    json.dump(config, f)

# Set env var for ADC to find it (in deployment or container)
# export GOOGLE_APPLICATION_CREDENTIALS=/etc/gcp/wif-config.json
```

### Per-User Impersonation in ADK

```python
# tools/bigquery_tools.py
from google.adk.tools import ToolContext
from google.cloud import bigquery
from google.auth import default, external_account
from google.auth.transport.requests import Request

def get_adc_credentials(wif_config_path: str = None):
    """Get ADC credentials. Supports both native GCP and WIF.
    
    Args:
        wif_config_path: Optional path to WIF credential config file
    
    Returns:
        Tuple of (credentials, project_id)
    """
    if wif_config_path and os.path.exists(wif_config_path):
        # Use WIF configuration
        with open(wif_config_path) as f:
            config = json.load(f)
        credentials = external_account.Credentials.from_info(config)
        credentials.refresh(Request())
        return credentials, config.get("quota_project_id")
    else:
        # Use native ADC
        return default()

def list_datasets(project_id: str, tool_context: ToolContext) -> dict:
    """List BigQuery datasets using ADC credentials."""
    # Get user's WIF config from state (set during auth)
    wif_config = tool_context.state.get("user:wif_config_path")
    
    try:
        credentials, _ = get_adc_credentials(wif_config)
        client = bigquery.Client(project=project_id, credentials=credentials)
        datasets = list(client.list_datasets())
        return {
            "datasets": [{"id": ds.dataset_id} for ds in datasets]
        }
    except Exception as e:
        return {"error": str(e)}

def query_bigquery(sql: str, project_id: str, tool_context: ToolContext) -> dict:
    """Query BigQuery using user's ADC credentials."""
    wif_config = tool_context.state.get("user:wif_config_path")
    access_level = tool_context.state.get("user:access_level", "read_only")
    
    # Validate for read-only users
    if access_level == "read_only" and not sql.strip().upper().startswith("SELECT"):
        return {"error": "Read-only users can only execute SELECT queries"}
    
    try:
        credentials, _ = get_adc_credentials(wif_config)
        client = bigquery.Client(project=project_id, credentials=credentials)
        results = client.query(sql).result()
        return {"rows": [dict(row) for row in results]}
    except Exception as e:
        return {"error": str(e)}
```

### User Authentication Flow

```python
# auth/user_auth.py
import msal
import json
from google.adk.tools import ToolContext

def authenticate_user(
    azure_tenant_id: str,
    azure_client_id: str,
    requested_role: str = "reader",
    tool_context: ToolContext
) -> dict:
    """Authenticate user and set up ADC-compatible WIF credentials.
    
    Args:
        azure_tenant_id: Azure tenant ID
        azure_client_id: Azure application ID  
        requested_role: 'reader' or 'admin' - determines which SA to impersonate
    """
    # Get Azure token via MSAL
    app = msal.PublicClientApplication(
        azure_client_id,
        authority=f"https://login.microsoftonline.com/{azure_tenant_id}"
    )
    
    # Acquire token interactively or silently
    result = app.acquire_token_interactive(scopes=["User.Read"])
    
    if "error" in result:
        return {"error": result.get("error_description", "Authentication failed")}
    
    # Determine service account based on user's Azure AD groups
    # In production, query user's group membership from MS Graph API
    user_groups = result.get("id_token_claims", {}).get("groups", [])
    
    if "bigquery-admins" in user_groups or requested_role == "admin":
        sa_email = "bq-admin@project.iam.gserviceaccount.com"
        access_level = "admin"
    else:
        sa_email = "bq-reader@project.iam.gserviceaccount.com"
        access_level = "read_only"
    
    # Create WIF config for ADC
    wif_config = {
        "type": "external_account",
        "audience": f"//iam.googleapis.com/projects/{project_id}/locations/global/workloadIdentityPools/azure-pool/providers/azure-provider",
        "subject_token_type": "urn:ietf:params:oauth:token-type:jwt",
        "token_url": "https://sts.googleapis.com/v1/token",
        "service_account_impersonation_url": (
            f"https://iamcredentials.googleapis.com/v1/projects/-/"
            f"serviceAccounts/{sa_email}:generateAccessToken"
        ),
        "credential_source": {
            "executable": {
                "command": "/usr/local/bin/azure-token-provider",
                "timeout_millis": 5000,
            }
        },
        "quota_project_id": project_id,
    }
    
    # Save config path to state
    config_path = f"/tmp/wif-config-{tool_context.state.get('session_id')}.json"
    with open(config_path, "w") as f:
        json.dump(wif_config, f)
    
    tool_context.state["user:wif_config_path"] = config_path
    tool_context.state["user:access_level"] = access_level
    tool_context.state["user:authenticated"] = True
    tool_context.state["user:service_account"] = sa_email
    
    return {
        "status": "authenticated",
        "service_account": sa_email,
        "access_level": access_level
    }
```

## OAuth 2.0 (User-Facing Apps)

Use OAuth when the agent needs to act on behalf of a user (Calendar, Gmail, Drive).

### OAuth 2.0 Authorization Code Flow

```python
# auth/oauth_manager.py
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import json
from google.adk.tools import ToolContext

SCOPES = {
    "calendar": ["https://www.googleapis.com/auth/calendar.readonly"],
    "gmail": ["https://www.googleapis.com/auth/gmail.readonly"],
    "bigquery": ["https://www.googleapis.com/auth/bigquery.readonly"],
}

class OAuthManager:
    """Manages OAuth 2.0 flows for user authorization."""
    
    def __init__(self, client_secrets_file: str):
        self.client_secrets_file = client_secrets_file
    
    def get_authorization_url(self, scope_type: str, redirect_uri: str) -> str:
        """Generate authorization URL for user consent."""
        flow = Flow.from_client_secrets_file(
            self.client_secrets_file,
            scopes=SCOPES.get(scope_type, []),
            redirect_uri=redirect_uri,
        )
        auth_url, _ = flow.authorization_url(prompt="consent")
        return auth_url
    
    def exchange_code(self, code: str, scope_type: str, redirect_uri: str) -> dict:
        """Exchange authorization code for credentials."""
        flow = Flow.from_client_secrets_file(
            self.client_secrets_file,
            scopes=SCOPES.get(scope_type, []),
            redirect_uri=redirect_uri,
        )
        flow.fetch_token(code=code)
        
        # Return credentials as serializable dict
        creds = flow.credentials
        return {
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": creds.scopes,
        }

def authorize_google_api(
    scope_type: str,
    authorization_code: str = None,
    tool_context: ToolContext
) -> dict:
    """Authorize Google API access for user."""
    oauth = OAuthManager("client_secrets.json")
    
    if not authorization_code:
        # Return authorization URL
        auth_url = oauth.get_authorization_url(
            scope_type=scope_type,
            redirect_uri="https://your-app.com/oauth/callback"
        )
        return {
            "status": "authorization_required",
            "authorization_url": auth_url
        }
    
    # Exchange code for credentials
    creds_dict = oauth.exchange_code(
        code=authorization_code,
        scope_type=scope_type,
        redirect_uri="https://your-app.com/oauth/callback"
    )
    
    # Store in state
    tool_context.state[f"user:oauth_creds:{scope_type}"] = creds_dict
    
    return {"status": "authorized", "scope": scope_type}
```

### Using OAuth Credentials

```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.adk.tools import ToolContext

def list_calendar_events(max_results: int = 10, tool_context: ToolContext) -> dict:
    """List user's calendar events using OAuth credentials."""
    creds_dict = tool_context.state.get("user:oauth_creds:calendar")
    if not creds_dict:
        return {"error": "Not authorized. Call authorize_google_api first."}
    
    # Reconstruct credentials from state
    credentials = Credentials(**creds_dict)
    
    # Refresh if expired
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
        # Update stored credentials
        tool_context.state["user:oauth_creds:calendar"] = {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes,
        }
    
    service = build("calendar", "v3", credentials=credentials)
    events = service.events().list(
        calendarId="primary",
        maxResults=max_results
    ).execute()
    
    return {"events": events.get("items", [])}
```

## Best Practices

### 1. Use ADC in Production - Never Service Account Keys

```python
# BAD: Using service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/key.json"

# GOOD: ADC automatically uses attached service account
# No configuration needed in production
from google.cloud import bigquery
client = bigquery.Client()  # Uses ADC
```

### 2. Configure Service Account Permissions

```bash
# Grant minimal permissions to the service account
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:my-agent@PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataViewer"  # Read-only, not Editor
```

### 3. Use WIF for Multi-Cloud - Not Keys

```python
# BAD: Downloading and using SA keys for Azure workloads
# GOOD: WIF with ADC - no keys needed, automatic token exchange
# Configure once, ADC handles the rest
```

### 4. Implement Token Refresh Automatically

```python
def get_refreshed_credentials(tool_context: ToolContext):
    """Get credentials with automatic refresh."""
    from google.auth import default
    from google.auth.transport.requests import Request
    
    credentials, project = default()
    
    if credentials.expired:
        credentials.refresh(Request())
    
    return credentials, project
```

### 5. Audit All Auth Events

```python
def audit_auth_event(event_type: str, user_id: str, details: dict, tool_context: ToolContext):
    """Log authentication events for security auditing."""
    import logging
    logger = logging.getLogger("adk.auth.audit")
    
    logger.info({
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "user_id": user_id,
        "session_id": tool_context.state.get("session_id"),
        "details": details,
    })
```

### 6. Validate Before Tool Execution

```python
def auth_guard(tool, args, tool_context):
    """Ensure user is authenticated and authorized."""
    if not tool_context.state.get("user:authenticated"):
        return {"error": "Authentication required"}
    
    if tool.name == "admin_operation":
        if tool_context.state.get("user:access_level") != "admin":
            return {"error": "Admin access required"}
    
    return None  # Proceed
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `DefaultCredentialsError` | Run `gcloud auth application-default login` locally, or attach SA in production |
| `Permission denied` | Check IAM bindings on service account, not just project |
| `invalid_grant` (OAuth) | Refresh token expired, user must re-authorize |
| `invalid_audience` (WIF) | Verify WIF provider audience URL matches config |
| Token expires quickly | Implement refresh logic using `credentials.refresh(Request())` |
| ADC not finding WIF | Ensure `GOOGLE_APPLICATION_CREDENTIALS` points to WIF config file |

## Deployment Checklist

- [ ] No service account key files in code or containers
- [ ] Service account attached to compute resource (Cloud Run, GKE, Agent Engine)
- [ ] Minimal IAM roles granted (principle of least privilege)
- [ ] WIF configuration stored as secret/config map, not in code
- [ ] OAuth credentials encrypted at rest
- [ ] Token refresh implemented for long-running sessions
- [ ] Audit logging enabled for auth events
