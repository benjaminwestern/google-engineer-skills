---
name: terraform-factory-patterns
version: "1.0.0"
description: Factory pattern design for Terraform including YAML-based configuration, discovery methods, defaults strategy, and use cases.
metadata:
  source_url: https://developer.hashicorp.com/terraform/docs
  docs_url: https://developer.hashicorp.com/terraform/docs
---

# Factory Pattern Design

> **Part of:** [terraform-skill](../SKILL.md)
> **Purpose:** YAML-based factory patterns for scalable infrastructure

This document describes the factory pattern approach—when to use it and how to implement it effectively.

---

## When to Use the Factory Pattern

### Decision: Traditional vs Factory

| Approach | Best For | Complexity |
|----------|----------|------------|
| **Traditional modules** | Unique resources, one-off setups | Lower |
| **Factory pattern** | Multiple similar resources, self-service needs | Higher |

**Use factory pattern when:**

- Creating multiple similar resources (projects, subnets, service accounts)
- Non-Terraform users need to provision infrastructure
- Want GitOps-style configuration management
- Need consistent defaults across many deployments

### The Core Idea

```bash
┌─────────────────────────────────────────────────────────────┐
│                    FACTORY PATTERN                          │
├─────────────────────────────────────────────────────────────┤
│  YAML Config → Discovery → Enrichment → Deployment          │
│     ↑            ↑           ↑            ↑                 │
│  Human-      fileset()    merge()      for_each           │
│  readable    yamldecode()  lookup()    module             │
│  config                                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Decisions

### Decision: Configuration Format

**YAML is preferred** for human-readable, version-controlled configs:

```yaml
# config/subnets.yaml
subnets:
  - name: app-us-central1
    region: us-central1
    ip_cidr_range: 10.0.0.0/24
  - name: db-us-central1
    region: us-central1
    ip_cidr_range: 10.0.1.0/24
```

**Alternative:** JSON for machine-generated configs, HCL for Terraform-native.

### Decision: Discovery Method

```hcl
# Option 1: Single config file (simpler)
locals {
  config = yamldecode(file("config/subnets.yaml"))
}

# Option 2: Auto-discovery (scalable)
locals {
  config_files = fileset(path.module, "config/**/*.yaml")
  configs = {
    for f in local.config_files :
    dirname(f) => yamldecode(file(f))
  }
}
```

**Choose single file for:** Simple setups, predictable configs
**Choose auto-discovery for:** Dynamic environments, user-driven configs

### Decision: Default Strategy

**Pattern:** Universal defaults → YAML overrides → explicit validation

```hcl
locals {
  # Parse raw configs
  raw = yamldecode(file("config/subnets.yaml"))
  
  # Enrich with defaults
  subnets = {
    for name, config in raw : name => {
      # Default values
      region      = lookup(config, "region", "us-central1")
      purpose     = lookup(config, "purpose", "PRIVATE")
      
      # Override with config
      ip_cidr_range = config.ip_cidr_range
      
      # Deep merge for nested structures
      labels = merge(
        { environment = "prod", managed_by = "terraform" },
        lookup(config, "labels", {})
      )
    }
  }
}
```

---

## Factory Patterns by Use Case

### Pattern 1: Project Factory

**Use case:** Multiple GCP projects with consistent setup

```yaml
# config/projects.yaml
project-api-prod:
  folder_id: "folders/1234567890"
  billing_account: "12345-67890-ABCDEF"
  services:
    - compute.googleapis.com
    - container.googleapis.com
  labels:
    environment: production
```

```hcl
locals {
  projects = yamldecode(file("config/projects.yaml"))
}

module "project" {
  source   = "terraform-google-modules/project-factory/google"
  for_each = local.projects
  
  name            = each.key
  folder_id       = each.value.folder_id
  billing_account = each.value.billing_account
  activate_apis   = each.value.services
  labels          = each.value.labels
}
```

### Pattern 2: Subnet Factory

**Use case:** Multiple subnets across regions with standard configuration

```yaml
# config/subnets.yaml
subnets:
  - name: app-us-central1
    region: us-central1
    ip_cidr_range: 10.0.0.0/24
    private_ip_google_access: true
  - name: db-us-central1
    region: us-central1
    ip_cidr_range: 10.0.1.0/24
```

```hcl
locals {
  subnets = yamldecode(file("config/subnets.yaml")).subnets
}

resource "google_compute_subnetwork" "subnets" {
  for_each = { for s in local.subnets : s.name => s }
  
  name          = each.value.name
  region        = each.value.region
  network       = var.vpc_id
  ip_cidr_range = each.value.ip_cidr_range
  
  private_ip_google_access = lookup(each.value, "private_ip_google_access", true)
}
```

### Pattern 3: Service Account Factory

**Use case:** Standardized service accounts with role assignments

```yaml
# config/service_accounts.yaml
service_accounts:
  ci-cd-runner:
    roles:
      - roles/storage.admin
      - roles/cloudbuild.builds.editor
  data-pipeline:
    roles:
      - roles/bigquery.dataEditor
      - roles/storage.objectViewer
```

```hcl
locals {
  service_accounts = yamldecode(file("config/service_accounts.yaml")).service_accounts
}

resource "google_service_account" "accounts" {
  for_each = local.service_accounts
  account_id = each.key
}

# Role assignment
resource "google_project_iam_member" "roles" {
  for_each = {
    for pair in setproduct(
      keys(local.service_accounts),
      flatten([for sa in local.service_accounts : sa.roles])
    ) : "${pair[0]}-${pair[1]}" => pair
  }
  
  role   = each.value[1]
  member = "serviceAccount:${google_service_account.accounts[each.value[0]].email}"
}
```

---

## Advanced Patterns

### Decision: Conditional Resource Creation

Create resources only when needed:

```hcl
resource "google_storage_bucket" "evaluation_datasets" {
  # Only create if flag is true AND agents need it
  count = var.create_evaluation_bucket && length(local.agents_with_evaluation) > 0 ? 1 : 0
  
  name     = "${var.project_id}-evaluation-datasets"
  location = var.region
}
```

### Decision: Lifecycle Hooks

Add cleanup logic for graceful teardown:

```hcl
resource "null_resource" "cleanup" {
  triggers = {
    resource_id = module.resource[each.key].id
  }
  
  provisioner "local-exec" {
    when    = destroy
    command = "gcloud resource delete ${self.triggers.resource_id} --quiet"
  }
}
```

---

## Factory Benefits

| Benefit | How It's Achieved |
|---------|-------------------|
| **Self-service** | YAML configs allow non-Terraform users |
| **GitOps** | All config version-controlled |
| **DRY** | Common patterns defined once |
| **Scalable** | Add resources by adding YAML files |
| **Maintainable** | Global changes via defaults |
| **Reviewable** | YAML diffs are easy to review |

---

## When NOT to Use Factory Pattern

Don't use when:

- Resources are unique with no common patterns
- Only one or two resources of a type
- Configuration changes frequently (YAML churn)
- Team prefers pure Terraform (no YAML abstraction)

---

**Back to:** [Main Skill File](../SKILL.md)
