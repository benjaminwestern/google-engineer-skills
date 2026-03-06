---
name: terraform-security-compliance
version: "1.0.0"
description: Security and compliance patterns for Terraform including OIDC authentication, secrets management, state security, and compliance testing tools.
metadata:
  source_url: https://developer.hashicorp.com/terraform/docs
  docs_url: https://developer.hashicorp.com/terraform/docs
---

# Security & Compliance

> **Part of:** [terraform-skill](../SKILL.md)
> **Purpose:** Security decisions and compliance patterns for Terraform

This document covers critical security choices. For secrets management patterns, see [code-patterns.md](code-patterns.md#secrets-management-strategy).

---

## Table of Contents

1. [Authentication Decision](#authentication-decision)
2. [Secrets Management](#secrets-management)
3. [Common Security Issues](#common-security-issues)
4. [State Security](#state-security)
5. [Compliance Testing](#compliance-testing)

---

## Authentication Decision

### The Choice: OIDC vs Service Account Keys

**Always choose OIDC.** No exceptions.

| Method | Security | Maintenance | Verdict |
|--------|----------|-------------|---------|
| **OIDC (Workload Identity)** | ✅ No long-lived credentials | ✅ Automatic | **USE THIS** |
| **Service Account Keys** | ❌ Long-lived, leak risk | ❌ Manual rotation | **NEVER** |

### OIDC Pattern (GitHub Actions)

```yaml
permissions:
  contents: 'read'
  id-token: 'write'  # Required for OIDC

jobs:
  deploy:
    steps:
      - uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: 'projects/PROJECT_ID/locations/global/workloadIdentityPools/POOL_ID/providers/PROVIDER_ID'
          service_account: 'terraform@PROJECT_ID.iam.gserviceaccount.com'
      
      - run: terraform plan
```

**For complete CI/CD examples, see [ci-cd-workflows.md](ci-cd-workflows.md#gcp-oidc-authentication-recommended).**

---

## Secrets Management

### The Decision: Where to Store Secrets

| Location | Safe? | Why |
|----------|-------|-----|
| **Google Secret Manager** | ✅ Yes | External to Terraform, referenced by data source |
| **Terraform state** | ❌ No | Plaintext JSON, readable by anyone with state access |
| **Variables** | ❌ No | Ends up in state |
| **random_password resource** | ❌ No | Result stored in state |

### The Pattern: Reference, Don't Store

```hcl
# ✅ GOOD - Secret stays in Secret Manager
data "google_secret_manager_secret_version" "db_password" {
  secret = "prod-database-password"
}

resource "google_sql_database_instance" "this" {
  root_password = data.google_secret_manager_secret_version.db_password.secret_data
}
```

**For write-only arguments (Terraform 1.11+), see [code-patterns.md](code-patterns.md#should-you-use-write-only-arguments).**

---

## Common Security Issues

### Decision: Network Architecture

| Approach | Risk Level | Recommendation |
|----------|------------|----------------|
| Default VPC | 🔴 High | Never use in production |
| Custom VPC with public subnets | 🟡 Medium | Use for public-facing services |
| Custom VPC with private subnets | 🟢 Low | Default choice |

```hcl
# ✅ GOOD - Private subnet
resource "google_compute_subnetwork" "private" {
  network                  = google_compute_network.this.id
  ip_cidr_range            = "10.0.1.0/24"
  private_ip_google_access = true
}
```

### Decision: Firewall Rules

| Rule | Risk | Verdict |
|------|------|---------|
| `source_ranges = ["0.0.0.0/0"]` | 🔴 Critical risk | Never for production |
| `ports = ["0-65535"]` | 🔴 Overly broad | Use specific ports |
| Specific ports + specific sources | 🟢 Least privilege | **Always prefer** |

```hcl
# ❌ BAD - Open to internet
resource "google_compute_firewall" "bad" {
  source_ranges = ["0.0.0.0/0"]
  allow { ports = ["0-65535"] }
}

# ✅ GOOD - Restricted
resource "google_compute_firewall" "good" {
  source_ranges = ["10.0.0.0/16"]
  allow { ports = ["443"] }
}
```

### Decision: Encryption

| Resource | Default Encryption | Recommendation |
|----------|-------------------|----------------|
| Cloud Storage | Google-managed | Use CMEK for sensitive data |
| Cloud SQL | Enabled | Verify encryption_key_name |
| Compute disks | Enabled | No action needed |

---

## State Security

### The Requirements

| Requirement | Implementation |
|-------------|----------------|
| **Encryption at rest** | Enable on GCS bucket |
| **Versioning** | Required for disaster recovery |
| **Access restriction** | Only Terraform service account |
| **No local state** | Always use remote backend |

```hcl
# backend.tf
terraform {
  backend "gcs" {
    bucket = "my-terraform-state"
    prefix = "prod/terraform.tfstate"
  }
}
```

### Secure State Bucket

```hcl
resource "google_storage_bucket" "terraform_state" {
  name     = "my-terraform-state"
  location = "US"

  versioning { enabled = true }
  encryption {
    default_kms_key_name = google_kms_crypto_key.terraform_state_key.id
  }
  uniform_bucket_level_access = true
}
```

---

## Compliance Testing

### Decision: Which Tool?

| Tool | Format | Best For |
|------|--------|----------|
| **trivy** | CLI + SARIF | Quick scans, CI integration |
| **checkov** | CLI + JSON | Policy-as-code, compliance |
| **OPA** | Rego | Complex policies, Kubernetes |

### Quick Start: trivy

```bash
# Scan configuration
trivy config .

# In CI
- uses: aquasecurity/trivy-action@master
  with:
    scan-type: 'config'
    scan-ref: '.'
```

---

**Back to:** [Main Skill File](../SKILL.md)
