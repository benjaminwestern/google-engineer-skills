---
name: terraform-code-patterns
version: "1.0.0"
description: Essential Terraform code patterns including count vs for_each, modern features (try, optional, moved), version management, and secrets handling.
metadata:
  source_url: https://developer.hashicorp.com/terraform/docs
  docs_url: https://developer.hashicorp.com/terraform/docs
---

# Code Patterns & Structure

> **Part of:** [terraform-skill](../SKILL.md)
> **Purpose:** Essential patterns and decision guides for Terraform code

This document covers the key choices you'll face when writing Terraform code and provides guidance on what to choose and why.

---

## The Seven Mantras (Detailed)

### 1. Always Have versions.tf

Every Terraform root module **must** have a `versions.tf` file that defines providers, their versions, and provider configuration. Never leave provider configuration implicit.

```hcl
# versions.tf
terraform {
  required_version = ">= 1.7.4"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 6.13.0, < 7.0.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = ">= 6.13.0, < 7.0.0"
    }
  }
}

# Provider configuration with ADC (no credentials block needed)
provider "google" {
  default_labels        = local.common_labels
  user_project_override = true
  billing_project       = var.billing_project
}

provider "google-beta" {
  default_labels        = local.common_labels
  user_project_override = true
  billing_project       = var.billing_project
}
```

### 2. Always Have backend.tf

Every root module **must** have a `backend.tf` file. It can start empty, but will eventually need remote state (prefer GCS for GCP).

```hcl
# backend.tf
terraform {
  backend "gcs" {
    bucket = "my-terraform-state"
    prefix = "org"
  }
}
```

### 3. Always Have locals.tf

Every module **must** have a `locals.tf` to define all local values for the entire module. Keep locals centralized, not scattered across files.

```hcl
# locals.tf
locals {
  labels = {
    stage = "org"
  }
  current_folder = basename(abspath(path.module))
}
```

### 4. Vertical Files by Domain

Organize resources into files by functional domain/workload, not by resource type. Each file should contain all related resources that form a complete "vertical" slice.

This pattern applies to ANY domain: web servers, managed instance groups, databases, ETL pipelines, API integrations, microservices, etc.

**Key Principle:** Each vertical file is self-contained and copy-paste friendly. To create a similar deployment, simply copy the file, rename it, update variables, and deploy.

```
# GOOD - Files organized by domain/workload:
├── networking.tf          # VPC, subnets, routes, firewall rules, NAT
├── webserver.tf           # MIG, template, LB, service account, secrets
├── salesforce-etl.tf      # SA, secrets, Cloud Function, Eventarc, BigQuery dataset
├── xero-etl.tf            # Same pattern as salesforce-etl.tf, different vars
├── api-gateway.tf         # Cloud Run, LB, service accounts, IAM
└── database.tf            # Cloud SQL, IAM, backups, monitoring

# BAD - Files organized by resource type:
├── iam.tf                # All IAM across all resources
├── compute.tf            # All compute resources mixed together
├── storage.tf            # All storage resources mixed together
```

**Cloud Foundation Fabric Integration:**

Leverage [Cloud Foundation Fabric](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric) modules inside these vertical files for production-ready GCP resources. Do NOT wrap these into custom modules—use CFF modules directly for maximum versatility and clarity.

```hcl
# salesforce-etl.tf - Complete vertical slice with CFF modules
module "salesforce_service_account" {
  source     = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/iam-service-account?ref=v53.0.0"
  project_id = var.project_id
  name       = "salesforce-etl"
}

module "salesforce_function" {
  source     = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/cloud-function-v2?ref=v53.0.0"
  project_id = var.project_id
  name       = "salesforce-to-bq"
  
  service_account = module.salesforce_service_account.email
  # ... function configuration
}

# secrets, eventarc triggers, etc. all in this one file
```

**Why this pattern?**

- **Maintainability:** Each file represents one complete workload—easy to understand and modify
- **Versatility:** Copy-paste to create similar deployments without module abstraction overhead
- **Clarity:** All dependencies for a workload live together
- **Team efficiency:** Developers can own entire verticals without cross-file coordination

### 5. Variables.tf with Sane Defaults and Examples

Not every module needs a `variables.tf`, but when it does:

- **Always provide sane defaults** - Don't force users to specify everything
- **Always provide example tfvars files** - Make usage patterns crystal clear

```hcl
# variables.tf with sensible defaults
variable "machine_type" {
  description = "GCE machine type"
  type        = string
  default     = "e2-micro"  # Sane default for dev/testing
  
  validation {
    condition     = can(regex("^[e-n]", var.machine_type))
    error_message = "Machine type must start with e or n (e2-standard, n2-standard, etc.)"
  }
}
```

```hcl
# terraform.tfvars.example
# Copy to terraform.tfvars and customize

# Production configuration
machine_type = "e2-standard-4"
min_replicas = 3
max_replicas = 10

# Development configuration (uncomment for dev)
# machine_type = "e2-micro"
# min_replicas = 1
# max_replicas = 2
```

### 6. YAML Factories for Heavy Reuse

When building modules with heavy reuse, create YAML factories so non-Terraform users can leverage the tooling easily.

```yaml
# config/projects.yaml
project-api-prod:
  folder_id: "folders/1234567890"
  billing_account: "12345-67890-ABCDEF"
  services:
    - compute.googleapis.com
    - storage.googleapis.com
    - logging.googleapis.com
  iam:
    "roles/viewer":
      - group:developers@example.com
    "roles/editor":
      - serviceAccount:ci-cd@example.com
  labels:
    environment: production
    team: platform
```

```hcl
# main.tf - Factory pattern
locals {
  projects = yamldecode(file("config/projects.yaml"))
}

module "project_factory" {
  source   = "terraform-google-modules/project-factory/google"
  for_each = local.projects

  name            = each.key
  billing_account = each.value.billing_account
  activate_apis   = each.value.services
  iam_bindings    = each.value.iam
  labels          = each.value.labels
}
```

**See [factory-patterns.md](factory-patterns.md) for detailed factory patterns.**

### 7. Repository Scope: Maximize Autonomy

**Golden Rule:** A repository's Terraform should manage **everything it owns** and **nothing it doesn't**. App deployments should not require changes to the foundations repository.

**Repository Ownership Model:**

```
# APP/AGENT REPO - Owns app-specific resources
agents-repo/
├── agents/
│   ├── customer-service.tf      # SA, secrets, Cloud Run, Eventarc
│   └── billing-agent.tf         # SA, secrets, Cloud Run, Eventarc
├── variables.tf                  # Per-agent configuration
└── terraform.tfvars              # Agent-specific settings

# FOUNDATIONS REPO - Owns shared infrastructure  
foundations-repo/
├── networking.tf                 # VPC, subnets, routes, NAT
├── load-balancer.tf              # Shared LB + routes (managed infrequently)
├── logging.tf                    # Central log sinks, exclusion filters
├── security.tf                   # Org policies, firewall rules
└── shared-buckets.tf             # Central audit logs, backups
```

**The Boundary Rule:**

Resources go in the **APP REPO** if they:

- Vary per deployment/instance
- Are created/modified frequently by app teams
- Need app-specific configuration
- Have independent deployment lifecycles

Resources go in the **FOUNDATIONS REPO** if they:

- Are shared across multiple apps/services
- Change infrequently (e.g., quarterly vs daily)
- Require platform/security team approval
- Provide the "substrate" (networking, logging, security baseline)

**Correct Split: Foundations Provides, Apps Consume**

```hcl
# GOOD: Foundations provides shared services, apps reference them
# foundations-repo/load-balancer.tf - Managed by platform team
resource "google_compute_url_map" "main" {
  name = "main-lb"
  # ... base configuration
}

# app-repo/main.tf - App deploys independently, references shared LB
module "api" {
  source = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/cloud-run-v2?ref=v53.0.0"
  name   = "my-api"
  
  # App creates its own route on the shared LB
  # via separate configuration or module parameters
}

# App deploys: Only touches app-repo
# LB updates: Platform team manages foundations-repo
```

**Anti-Pattern to Avoid:**

```
# BAD: App deployment requires foundations repo changes
# App team wants new route → must PR to foundations repo
# App team needs firewall rule → blocked on platform team
# Result: Every app deployment requires cross-team coordination
```

**Why this matters:**

- **Team velocity:** App teams deploy daily without waiting for foundations changes
- **Appropriate governance:** Platform team controls shared infrastructure (quarterly)
- **Clear ownership:** Foundations = shared substrate, Apps = business logic
- **Independent lifecycles:** Different deployment frequencies don't block each other

---

## Table of Contents

1. [Count vs For_Each: The Critical Choice](#count-vs-for_each-the-critical-choice)
2. [Block Ordering Rules](#block-ordering-rules)
3. [Modern Features Decision Guide](#modern-features-decision-guide)
4. [Version Constraints](#version-constraints)
5. [Secrets Management Strategy](#secrets-management-strategy)
6. [Refactoring Patterns](#refactoring-patterns)

---

## Count vs For_Each: The Critical Choice

This is the most important structural decision in Terraform. Choose wrong and you'll face painful resource recreation later.

### When to use `count`

✅ **Simple numeric replication** - Creating N identical resources where order doesn't matter and items won't change:

```hcl
resource "google_compute_subnetwork" "public" {
  count = 3
  ip_cidr_range = cidrsubnet(var.vpc_cidr, 8, count.index)
}
```

✅ **Boolean conditions** - Create or don't create a resource:

```hcl
resource "google_compute_router_nat" "this" {
  count = var.create_nat_gateway ? 1 : 0
}
```

### When to use `for_each`

✅ **Items have natural keys** - Resources should be addressable by meaningful names:

```hcl
resource "google_compute_subnetwork" "private" {
  for_each = toset(var.zones)  # ["us-central1-a", "us-central1-b"]
  
  zone = each.key
}
# Reference: google_compute_subnetwork.private["us-central1-a"]
```

✅ **Items may be added/removed from middle** - The list can change:

```hcl
# ❌ BAD with count: Removing "us-central1-b" would recreate "us-central1-c"
# ✅ GOOD with for_each: Removal only affects that specific resource
resource "google_compute_subnetwork" "private" {
  for_each = toset(var.zones)
  zone     = each.key
}
```

### Decision Flowchart

```bash
Do resources need meaningful identifiers?
│
├─ YES → for_each (with set or map)
│
└─ NO → Can items change position in the list?
    ├─ YES → for_each (prevents recreation cascade)
    └─ NO → count (simpler for fixed N items)
```

### Migration: Count to For_Each

If you need to migrate from `count` to `for_each`, use `moved` blocks to prevent recreation:

```hcl
# Before
resource "google_compute_subnetwork" "private" {
  count = length(var.zones)
  zone  = var.zones[count.index]
}

# After
resource "google_compute_subnetwork" "private" {
  for_each = toset(var.zones)
  zone     = each.key
}

# Prevent recreation of existing resources
moved {
  from = google_compute_subnetwork.private[0]
  to   = google_compute_subnetwork.private["us-central1-a"]
}
```

---

## Block Ordering Rules

Consistent ordering prevents errors and makes code easier to read.

### Resource Block Order

```hcl
resource "google_compute_instance" "this" {
  # 1. Meta-arguments FIRST
  count = var.instance_count
  
  # 2. Required arguments
  name         = var.name
  machine_type = var.machine_type
  
  # 3. Tags/labels (last real argument)
  labels = var.labels
  
  # 4. depends_on (if needed)
  depends_on = [google_compute_network.this]
  
  # 5. lifecycle (if needed)
  lifecycle {
    create_before_destroy = true
  }
}
```

### Variable Block Order

```hcl
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
  sensitive   = false
  nullable    = false
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Must be dev, staging, or prod."
  }
}
```

---

## Modern Features Decision Guide

### Should You Use `try()`?

**Yes**, always prefer `try()` over the legacy `element(concat())` pattern:

```hcl
# ✅ MODERN - Clean and readable
output "firewall_id" {
  value = try(google_compute_firewall.this[0].id, "")
}

# ❌ LEGACY - Hard to read
output "firewall_id" {
  value = element(concat(google_compute_firewall.this.*.id, [""]), 0)
}
```

### Should You Use `optional()`?

**Yes, if using Terraform 1.3+**. It simplifies object type definitions:

```hcl
# Without optional() - all fields required
variable "config" {
  type = object({
    name     = string
    size     = number
    enabled  = bool  # Must always provide this
  })
}

# With optional() - sensible defaults
variable "config" {
  type = object({
    name     = string
    size     = optional(number, 100)
    enabled  = optional(bool, true)
  })
}
# Usage: config = { name = "myapp" }  # size and enabled use defaults
```

### Should You Use `nullable = false`?

**Yes, if using Terraform 1.1+** and the variable should never be null:

```hcl
variable "vpc_cidr" {
  type     = string
  nullable = false  # Passing null uses default, not null
  default  = "10.0.0.0/16"
}
```

### Should You Use `moved` Blocks?

**Yes, when refactoring** to rename resources or migrate between count/for_each:

```hcl
# Rename a resource
moved {
  from = google_compute_instance.web_server
  to   = google_compute_instance.web
}

# Migrate to for_each
moved {
  from = google_compute_subnetwork.private[0]
  to   = google_compute_subnetwork.private["us-central1-a"]
}
```

### Should You Use Write-Only Arguments?

**Yes, if using Terraform 1.11+** for secrets. They prevent secrets from appearing in state:

```hcl
# ✅ GOOD - Secret is write-only, not stored in state
resource "google_sql_database_instance" "this" {
  root_password = data.google_secret_manager_secret_version.db_password.secret_data
}
```

---

## Version Constraints

### Decision: How Strict Should You Be?

| Component | Recommendation | Why |
|-----------|----------------|-----|
| **Terraform** | `~> 1.9` | Allows patch updates, predictable |
| **Providers** | `~> 5.0` | Allows minor/patch updates |
| **Modules (prod)** | Exact version | Stability over flexibility |
| **Modules (dev)** | `~> 5.0` | Allow updates for testing |

### Syntax Guide

```hcl
# ❌ Too rigid - prevents security patches
version = "5.0.0"

# ✅ Recommended - allows patches within major version
version = "~> 5.0"

# Also valid - explicit range
version = ">= 5.0, < 6.0"
```

### Update Strategy

```bash
Security patches: Update immediately, test quickly
Minor versions:   Monthly maintenance windows
Major versions:   Planned upgrade cycles with testing
```

---

## Secrets Management Strategy

### The Rule: Never Store Secrets in State

**Why:** Terraform state files are plaintext JSON. Anyone with access can read secrets.

### Option 1: Create Secrets with Write-Only Arguments (Terraform 1.11+)

Terraform 1.11+ introduces write-only arguments that allow creating secrets without storing them in state. This is the **recommended approach** when using CFF modules.

```hcl
# Using Cloud Foundation Fabric module with write-only arguments
module "db_credentials" {
  source = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/secret-manager?ref=v36.0.0"
  
  project_id = var.project_id
  name       = "db-password"
  
  # The secret value is marked as write-only
  # Terraform creates it but never stores it in state
  secret_value = {
    write_only = true
    value      = var.db_password  # Only used during creation, not stored
  }
}

# Reference the secret in other resources
data "google_secret_manager_secret_version" "db_password" {
  secret = module.db_credentials.secret_id
}

resource "google_sql_database_instance" "this" {
  root_password = data.google_secret_manager_secret_version.db_password.secret_data
}
```

**Benefits:**
- Secrets created entirely in Terraform
- Values never appear in state
- Compatible with CFF modules
- No manual gcloud commands needed

### Option 2: Reference Existing Secrets

Create secrets outside Terraform (via gcloud, console, or another process), then reference them:

```hcl
# 1. Create secret in Google Secret Manager (outside Terraform)
#    gcloud secrets create prod-db-password --data-file=- <<< "your-password"

# 2. Reference it in Terraform
data "google_secret_manager_secret_version" "db_password" {
  secret = "prod-database-password"
}

resource "google_sql_database_instance" "this" {
  root_password = data.google_secret_manager_secret_version.db_password.secret_data
}
```

**Use when:**
- Using Terraform < 1.11
- Secrets created by external systems
- Manual secret rotation workflows

### What NOT To Do

```hcl
# ❌ BAD - Secret ends up in state
resource "random_password" "db" {
  length = 16
}

resource "google_sql_database_instance" "this" {
  root_password = random_password.db.result  # Stored in state!
}

# ❌ BAD - Variable secret also in state
variable "db_password" {
  type = string
}

resource "google_sql_database_instance" "this" {
  root_password = var.db_password  # Still in state
}
```

---

## Refactoring Patterns

### When to Refactor

- **Resource addressing issues** - Using count when you need for_each
- **Naming improvements** - Resource names that don't reflect purpose
- **Module reorganization** - Splitting or combining modules
- **Modernization** - Upgrading from 0.12/0.13 syntax

### Pattern: Migrate from 0.12/0.13 to 1.x

**Replace these legacy patterns:**

| Old Pattern | Modern Replacement | Version |
|-------------|-------------------|---------|
| `element(concat(...))` | `try()` | 0.13+ |
| `list` type | `list()` function | 0.12+ |
| No validation | `validation` blocks | 0.13+ |
| Complex workarounds | `optional()` | 1.3+ |
| Resource recreation on rename | `moved` blocks | 1.1+ |
| Secrets in state | Write-only arguments | 1.11+ |

### Pattern: Secrets Remediation

**Goal:** Move existing secrets out of state

```bash
# 1. Create secret in Google Secret Manager (outside Terraform)
gcloud secrets create prod-db-password --data-file=- <<< "your-password"

# 2. Update Terraform to use data sources instead of variables/resources

# 3. Apply changes
terraform apply

# 4. Verify secret not in state
terraform show | grep -i password  # Should return nothing
```

---

**Back to:** [Main Skill File](../SKILL.md)
