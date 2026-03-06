---
name: terraform-module-patterns
version: "1.0.0"
description: Module development patterns for Terraform including resource modules, infrastructure modules, composition, naming conventions, and anti-patterns.
metadata:
  source_url: https://developer.hashicorp.com/terraform/docs
  docs_url: https://developer.hashicorp.com/terraform/docs
---

# Module Development Patterns

> **Part of:** [terraform-skill](../SKILL.md)
> **Purpose:** Decision guide for Terraform module development

This document helps you make the right choices when creating modules. For syntax patterns, see [code-patterns.md](code-patterns.md). For testing strategies, see [testing-frameworks.md](testing-frameworks.md).

---

## Module Type Decision

### The Three Types (Most to Least Reusable)

| Type | Decision Question | Example |
|------|-------------------|---------|
| **Resource Module** | Is this a focused group of related resources? | VPC + subnets, IAM role + policies |
| **Infrastructure Module** | Does it combine multiple infrastructure concerns? | Complete networking stack |
| **Composition** | Is this environment-specific configuration? | Production environment setup |

### Decision Flowchart

```bash
Is this environment-specific configuration?
├─ YES → Composition (environments/prod/)
└─ NO  → Does it combine multiple concerns?
    ├─ YES → Infrastructure Module (modules/web-app/)
    └─ NO  → Resource Module (modules/vpc/)
```

---

## Architecture Decisions

### Decision: Module Scope Size

**Small scopes = better performance + reduced blast radius**

```bash
# ✅ GOOD: Separated by concern
environments/prod/
  networking/     # VPC, subnets
  compute/        # GCE, load balancers
  data/           # Cloud SQL
  
# ❌ BAD: Everything in one module
environments/prod/
  everything.tf   # 2000 lines, manages everything
```

### Decision: How to Connect Modules

| Method | Coupling | Best For |
|--------|----------|----------|
| **Module outputs** | Tight | Same codebase, same team |
| **Remote state** | Loose | Separate teams, separate repos |

```hcl
# Option 1: Module outputs (tight coupling)
module "vpc" { source = "../../modules/vpc" }
module "gce" {
  source     = "../../modules/gce"
  network_id = module.vpc.network_id
}

# Option 2: Remote state (loose coupling)
data "terraform_remote_state" "vpc" { ... }
module "gce" {
  source     = "../../modules/gce"
  network_id = data.terraform_remote_state.vpc.outputs.network_id
}
```

### Decision: What Goes Where

| File | Rule |
|------|------|
| `main.tf` | Resource definitions only |
| `variables.tf` | All inputs with descriptions |
| `outputs.tf` | All outputs with descriptions |
| `versions.tf` | Provider constraints |
| `backend.tf` | **ONLY** at composition level |
| `terraform.tfvars` | **NEVER** in reusable modules |

---

## Module Design Decisions

### Decision: Parameterize vs Hardcode

**Always parameterize values that change between environments:**

```hcl
# ✅ GOOD - Configurable
resource "google_compute_instance" "web" {
  machine_type = var.machine_type
  labels       = var.labels
}

# ❌ BAD - Locked to specific values
resource "google_compute_instance" "web" {
  machine_type = "e2-standard-2"
  labels       = { environment = "production" }
}
```

### Decision: Root Module vs Reusable Module

| | Root Module | Reusable Module |
|---|-------------|-----------------|
| **Purpose** | Environment-specific | Generic, reusable |
| **Values** | Concrete, hardcoded | Variables, parameterized |
| **Location** | `environments/prod/` | `modules/vpc/` |

```hcl
# Root module (environment-specific)
# environments/prod/main.tf
module "vpc" {
  source       = "../../modules/vpc"
  network_name = "prod-vpc"  # Concrete value
}

# Reusable module (generic)
# modules/vpc/main.tf
resource "google_compute_network" "this" {
  name = var.network_name  # Parameterized
}
```

---

## Naming Decisions

### Decision: Variable Naming

**Use context-specific names, not generic:**

```hcl
# ✅ Good
var.vpc_cidr_block          # Context: VPC
var.database_instance_class # Context: Database

# ❌ Bad
var.cidr                    # Too generic
var.instance_class          # Too generic
```

### Decision: Output Naming Pattern

**Pattern:** `{name}_{type}_{attribute}`

```hcl
# ✅ GOOD
output "firewall_rule_id" {
  value = try(google_compute_firewall.this[0].id, "")
}

output "private_subnet_ids" {  # Plural for lists
  value = google_compute_subnetwork.private[*].id
}
```

---

## Anti-Patterns to Avoid

### ❌ God Modules

```hcl
# Bad: One module does everything
module "everything" {
  source = "./modules/app-infrastructure"
  # Creates VPC, GCE, Cloud SQL, Storage, IAM...
}

# Fix: Focused modules
module "networking" { source = "./modules/vpc" }
module "compute" { 
  source     = "./modules/gce"
  network_id = module.networking.network_id
}
```

### ❌ Environment Sprawl in Root Module

```hcl
# Bad: All environments in one place
resource "google_compute_instance" "app" {
  for_each = toset(["dev", "staging", "prod"])
}

# Fix: Separate root modules
environments/
  dev/main.tf
  staging/main.tf  
  prod/main.tf
```

---

## Testing Decisions

### Decision: What to Test

| Test Type | What It Validates |
|-----------|-------------------|
| **Input validation** | Variables accept/reject correct values |
| **Idempotency** | Second apply shows "No changes" |
| **Destroy completeness** | All resources cleaned up |

### Decision: Test Framework

See [testing-frameworks.md](testing-frameworks.md#testing-strategy-overview) for the decision flowchart.

**Quick answer:**

- Simple logic + HCL team → Native tests (Terraform 1.6+)
- Complex integration + Go team → Terratest

---

**Back to:** [Main Skill File](../SKILL.md)
