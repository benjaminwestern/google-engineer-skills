---
name: terraform-ci-cd-workflows
version: "1.0.0"
description: CI/CD workflow patterns for Terraform including OIDC authentication, apply strategies, environment organization, and Atlantis integration.
metadata:
  source_url: https://developer.hashicorp.com/terraform/docs
  docs_url: https://developer.hashicorp.com/terraform/docs
---

# CI/CD Workflows for Terraform

> **Part of:** [terraform-skill](../SKILL.md)
> **Purpose:** CI/CD integration patterns and decisions for Terraform

This document covers the key CI/CD decisions you'll face and provides recommended patterns.

---

## Table of Contents

1. [The Core Workflow Decision](#the-core-workflow-decision)
2. [Authentication: The Critical Choice](#authentication-the-critical-choice)
3. [Apply Strategy: Manual vs Automatic](#apply-strategy-manual-vs-automatic)
4. [Environment Organization](#environment-organization)
5. [Atlantis Integration](#atlantis-integration)

---

## The Core Workflow Decision

### Standard Pipeline: Validate → Plan → Apply

```yaml
# .github/workflows/terraform.yml
name: Terraform

on: [push, pull_request]

permissions:
  contents: 'read'
  id-token: 'write'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      
      - run: terraform fmt -check -recursive
      - run: terraform init
      - run: terraform validate

  plan:
    needs: validate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      
      - run: terraform init
      - run: terraform plan -out=tfplan
      
      # Optional: Post plan to PR
      - uses: marocchino/sticky-pull-request-comment@v2
        with:
          header: plan
          message: |
            #### Terraform Plan
            ```
            ${{ steps.plan.outputs.stdout }}
            ```

  apply:
    needs: plan
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production  # Requires approval
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      
      - run: terraform init
      - run: terraform apply -auto-approve tfplan
```

---

## Authentication: The Critical Choice

### Decision: How to Authenticate with GCP

**Always choose OIDC over service account keys.**

| Method | Security | Maintenance | Recommendation |
|--------|----------|-------------|----------------|
| **OIDC (Workload Identity)** | ✅ No long-lived credentials | ✅ Automatic rotation | **Use this** |
| **Service Account Keys** | ❌ Long-lived, leak risk | ❌ Manual rotation | Never use |

### OIDC Authentication Pattern

```yaml
permissions:
  contents: 'read'
  id-token: 'write'  # Required for OIDC

jobs:
  deploy:
    steps:
      - id: 'auth'
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: 'projects/PROJECT_ID/locations/global/workloadIdentityPools/POOL_ID/providers/PROVIDER_ID'
          service_account: 'terraform@PROJECT_ID.iam.gserviceaccount.com'
      
      # Now terraform commands use this authentication
      - run: terraform init
      - run: terraform plan
```

**See [security-compliance.md](security-compliance.md#gcp-authentication-security) for OIDC setup details.**

---

## Apply Strategy: Manual vs Automatic

### Decision: When Should Apply Run?

| Strategy | Safety | Speed | Best For |
|----------|--------|-------|----------|
| **Push to main** | ⚠️ Medium | ✅ Fast | Dev/staging, trusted team |
| **PR approval required** | ✅ High | ⚠️ Slower | Production, compliance |
| **Comment-triggered** | ✅ High | ⚠️ Manual | Production, extra control |

### Option 1: Push to Main (Fast)

```yaml
apply:
  needs: plan
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
  environment: production  # Still requires manual approval via GitHub environments
  steps:
    - run: terraform apply -auto-approve tfplan
```

### Option 2: Comment-Triggered (Controlled)

```yaml
# Trigger apply with PR comment: /terraform_apply
on:
  issue_comment:
    types: [created]

jobs:
  check-comment:
    if: github.event.issue.pull_request && contains(github.event.comment.body, '/terraform_apply')
    runs-on: ubuntu-latest
    steps:
      - name: Check approvals
        run: |
          # Verify PR has required approvals before proceeding
          # Implementation depends on your requirements
          
  apply:
    needs: check-comment
    runs-on: ubuntu-latest
    steps:
      - run: terraform apply -auto-approve
```

---

## Environment Organization

### Decision: One Workflow or Many?

**Option A: Separate workflows per environment**

```
.github/workflows/
  terraform-dev.yml      # Auto-apply on push
  terraform-staging.yml  # Auto-apply on push  
  terraform-prod.yml     # Requires approval
```

**Pros:** Simple, clear, independent
**Cons:** Duplicated code

**Option B: Reusable workflow**

```yaml
# .github/workflows/terraform-deploy.yml
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      auto_apply:
        required: true
        type: boolean

jobs:
  deploy:
    environment: ${{ inputs.environment }}
    steps:
      - run: terraform init
      - run: terraform plan -out=tfplan
      - if: inputs.auto_apply
        run: terraform apply -auto-approve tfplan
```

**Called by:**

```yaml
# .github/workflows/prod.yml
jobs:
  deploy:
    uses: ./.github/workflows/terraform-deploy.yml
    with:
      environment: production
      auto_apply: false
```

**Pros:** DRY, centralized changes
**Cons:** More complex, harder to debug

**Recommendation:** Start with separate workflows, refactor to reusable when you have 3+ environments with identical steps.

---

## CI/CD Best Practices

### Essential Security Checks

```yaml
# Add to validate or plan job
- name: Security Scan
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: 'config'
    scan-ref: '.'
```

### State Locking

```yaml
# Prevent concurrent runs
terraform apply -lock-timeout=10m tfplan
```

### Plugin Caching

```yaml
- uses: actions/cache@v3
  with:
    path: ~/.terraform.d/plugin-cache
    key: ${{ runner.os }}-terraform-${{ hashFiles('**/.terraform.lock.hcl') }}
```

---

## Atlantis Integration

### Decision: GitHub Actions vs Atlantis?

| Feature | GitHub Actions | Atlantis |
|---------|---------------|----------|
| Native integration | ✅ Built-in | ⚠️ Additional service |
| Plan in PR comments | ⚠️ Requires action | ✅ Native |
| Apply from PR | ⚠️ Requires setup | ✅ Native (`atlantis apply`) |
| Multi-repo support | ⚠️ Workflow per repo | ✅ Single instance |
| Cost | ✅ Free (GitHub) | ⚠️ Infrastructure cost |

**Use GitHub Actions when:** Simple setup, single repo, standard workflows
**Use Atlantis when:** Multiple repos, need plan/apply in PR comments, centralized control

### Atlantis Configuration

```yaml
# atlantis.yaml
version: 3
parallel_plan: true
parallel_apply: true

projects:
  - name: "networking"
    dir: "environments/prod/networking"
    autoplan:
      when_modified: ["**/*.tf"]
  
  - name: "compute"
    dir: "environments/prod/compute"
    autoplan:
      when_modified: ["**/*.tf"]
```

**Usage:**

```
# In PR comment
atlantis plan    # Shows plan in PR comment
atlantis apply   # Applies changes
```

**Atlantis works seamlessly with OIDC** - no additional credentials needed.

---

## Quick Decision Checklist

Setting up a new pipeline? Answer these:

- [ ] **Authentication:** Using OIDC? (Should be YES)
- [ ] **Environment strategy:** Separate workflows or reusable? (Start with separate)
- [ ] **Apply trigger:** Push, approval, or comment? (Production = approval or comment)
- [ ] **Security scanning:** Trivy or Checkov included? (Should be YES)
- [ ] **State backend:** Remote with locking? (Should be YES)

---

**Back to:** [Main Skill File](../SKILL.md)
