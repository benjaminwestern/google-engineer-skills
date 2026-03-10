---
name: terraform
version: "1.0.0"
description: >
  MUST USE when creating, reviewing, testing, or refactoring Terraform code.
  Covers modules, providers, resources, variables, CI/CD workflows, policy and
  validation patterns, and infrastructure-as-code design decisions. Do NOT use
  for imperative cloud CLI tasks or non-Terraform deployment tooling unless the
  task explicitly requires Terraform.
metadata:
  source_url: https://github.com/hashicorp/terraform
  docs_url: https://developer.hashicorp.com/terraform/docs
---

# Terraform Skill

Comprehensive Terraform guidance covering modules, testing, CI/CD, and production patterns. Combines best practices from terraform-best-practices.com and Cloud Foundation Fabric.

---

## The Seven Mantras

These principles guide all Terraform work:

1. **Always Have versions.tf** — Every root module must define providers, versions, and configuration. Never leave provider config implicit.
2. **Always Have backend.tf** — Even if empty initially, you'll need remote state (GCS for GCP).
3. **Always Have locals.tf** — Centralize all local values, don't scatter them across files.
4. **Vertical Files by Domain** — Organize by workload (webserver.tf, salesforce-etl.tf), not by resource type (iam.tf, compute.tf).
5. **Variables with Sane Defaults** — Provide sensible defaults and example tfvars files.
6. **YAML Factories for Heavy Reuse** — Enable non-Terraform users via YAML configs + factory patterns.
7. **Maximize Autonomy** — App repos own their resources, foundations repos own shared infrastructure. Avoid cross-repo dependencies.

---

## Core Principles

### 1. Required Files

Every Terraform root module **must** have:

| File | Purpose |
|------|---------|
| `versions.tf` | Provider versions and configuration |
| `backend.tf` | Remote state (even if empty initially) |
| `locals.tf` | Centralized local values |
| `variables.tf` | Input variables (when needed) |

### 2. Vertical File Organization

Organize by domain/workload, not by resource type:

```
# GOOD - Files by domain:
├── networking.tf      # VPC, subnets, routes, NAT
├── webserver.tf       # MIG, template, LB, service account
├── salesforce-etl.tf  # SA, secrets, Cloud Function, BigQuery
└── database.tf        # Cloud SQL, IAM, backups

# BAD - Files by resource type:
├── iam.tf            # All IAM mixed together
├── compute.tf        # All compute mixed together
└── storage.tf        # All storage mixed together
```

### 3. Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| **Resources** | Descriptive, contextual | `web_server`, `application_logs` |
| **Singletons** | Use `this` | `google_compute_network.this` |
| **Variables** | Context-specific | `vpc_cidr_block`, `database_instance_class` |
| **Outputs** | `{name}_{type}_{attribute}` | `firewall_rule_id`, `subnet_ids` |

### 4. Module Boundaries

| Type | Scope | Example |
|------|-------|---------|
| **Resource Module** | Single logical group | VPC + subnets |
| **Infrastructure Module** | Collection of resources | Complete networking stack |
| **Composition** | Environment-specific | Production environment |
| **Repository** | Owns its resources | App repo = app resources only |

---

## Quick Decision Reference

### Count vs For_Each

```
Do resources need meaningful identifiers?
│
├─ YES → for_each (with set or map)
│
└─ NO → Can items change position?
    ├─ YES → for_each (prevents cascade)
    └─ NO → count (simpler)
```

**See [code-patterns.md](references/code-patterns.md) for migration patterns and detailed examples.**

### Testing Approach

```
What do you need to test?
│
├─ Syntax/format? → terraform validate + fmt
├─ Security? → trivy + checkov
├─ Simple logic (1.6+)? → Native tests
└─ Complex integration? → Terratest
```

**See [testing-frameworks.md](references/testing-frameworks.md) for implementation details.**

### Authentication (GCP)

**Always use OIDC. Never use service account keys.**

| Method | Security | Use Case |
|--------|----------|----------|
| **OIDC** | ✅ No long-lived credentials | CI/CD (GitHub Actions) |
| **ADC** | ✅ User credentials | Local development |
| **Impersonation** | ✅ Service account delegation | Automation |
| **Keys** | ❌ Long-lived risk | Never use |

**See [security-compliance.md](references/security-compliance.md) for OIDC setup and security patterns.**

---

## Modern Features (Quick Reference)

| Feature | Version | When to Use |
|---------|---------|-------------|
| `try()` | 0.13+ | Safe fallbacks (always use) |
| `optional()` | 1.3+ | Optional object attributes |
| `moved` blocks | 1.1+ | Refactor without recreation |
| Native tests | 1.6+ | Unit testing in HCL |
| Mock providers | 1.7+ | Cost-free testing |
| Write-only args | 1.11+ | Secrets (never in state) |

---

## Essential Commands

```bash
# Static analysis (always free)
terraform fmt -recursive -check
terraform validate
tflint
trivy config .
checkov -d .

# Testing (1.6+)
terraform test

# Plan and apply
terraform plan -out=tfplan
terraform apply -auto-approve tfplan

# State management
terraform state list
terraform show
```

**See [quick-reference.md](references/quick-reference.md) for full cheat sheet.**

---

## Security Checklist

- [ ] **Authentication:** Using OIDC (not keys)
- [ ] **Secrets:** In Secret Manager (not state/variables)
- [ ] **Network:** Custom VPC (not default)
- [ ] **Firewall:** Least privilege (not 0.0.0.0/0)
- [ ] **State:** Encrypted, versioned, restricted access
- [ ] **Scanning:** Trivy/Checkov in CI/CD

**See [security-compliance.md](references/security-compliance.md) for detailed patterns.**

---

## Module Checklist

- [ ] `versions.tf` with provider constraints
- [ ] `backend.tf` for remote state
- [ ] `variables.tf` with descriptions and validation
- [ ] `outputs.tf` with descriptions
- [ ] `examples/` directory (simple and complete)
- [ ] Tests (native 1.6+ or Terratest)
- [ ] Pre-commit hooks configured
- [ ] Documentation in README.md

**See [module-patterns.md](references/module-patterns.md) for details.**

---

## CI/CD Essentials

### Standard Pipeline

```yaml
validate → plan → apply
```

### Key Decisions

| Decision | Recommendation |
|----------|----------------|
| **Authentication** | OIDC (never keys) |
| **Apply trigger** | Push for dev/staging, approval for prod |
| **Workspaces** | Separate files per environment |
| **Security scan** | Trivy + Checkov in CI |

**See [ci-cd-workflows.md](references/ci-cd-workflows.md) for templates.**

---

## Reference Documentation

### [code-patterns.md](references/code-patterns.md)
**When to use:** Writing or refactoring Terraform code

**Covers:**
- Count vs for_each decision guide and migration patterns
- Block ordering rules (resources, variables)
- Modern features decision guide (try, optional, moved, write-only)
- Version constraints and update strategy
- Secrets management patterns
- Refactoring from legacy (0.12/0.13) to modern syntax

### [quick-reference.md](references/quick-reference.md)
**When to use:** Need quick lookup or troubleshooting

**Covers:**
- Command cheat sheet (format, validate, test, plan)
- Decision flowcharts (testing, module workflow, refactoring)
- Version-specific guidance (1.0-1.5, 1.6+, 1.7+)
- Troubleshooting common issues
- Version constraint syntax reference

### [module-patterns.md](references/module-patterns.md)
**When to use:** Creating or restructuring modules

**Covers:**
- Module type decision tree (Resource → Infrastructure → Composition)
- Architecture decisions (scope size, module connections)
- File organization standards
- Parameterization vs hardcoding
- Root module vs reusable module boundaries
- Naming decisions (variables, outputs)
- Anti-patterns to avoid (god modules, environment sprawl)

### [testing-frameworks.md](references/testing-frameworks.md)
**When to use:** Setting up or choosing testing approach

**Covers:**
- Testing decision flowchart
- Native tests vs Terratest comparison
- Critical plan vs apply decision
- Working with set-type blocks
- Mocking decisions
- Terratest patterns and cost management
- Testing checklist

### [ci-cd-workflows.md](references/ci-cd-workflows.md)
**When to use:** Setting up CI/CD pipelines

**Covers:**
- Standard validate → plan → apply pipeline
- OIDC authentication patterns
- Apply strategy options (push, approval, comment-triggered)
- Environment organization (separate vs reusable workflows)
- Essential security checks in CI
- Atlantis integration decision guide

### [security-compliance.md](references/security-compliance.md)
**When to use:** Security review or compliance setup

**Covers:**
- OIDC vs service account key decision
- Secrets management (what's safe vs unsafe)
- Network architecture decisions
- Firewall rule best practices
- State security requirements
- Compliance testing tools (trivy, checkov, terraform-compliance, OPA)

### [factory-patterns.md](references/factory-patterns.md)
**When to use:** Building scalable, self-service infrastructure

**Covers:**
- When to use factory vs traditional modules
- Configuration format decisions (YAML vs JSON)
- Discovery methods (single file vs auto-discovery)
- Default strategy patterns
- Factory patterns by use case (Project, Subnet, Service Account)
- Conditional resource creation
- Lifecycle hooks
- When NOT to use factory pattern

---

Based on:
- [Cloud Foundation Fabric](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric) by Google Cloud Platform
