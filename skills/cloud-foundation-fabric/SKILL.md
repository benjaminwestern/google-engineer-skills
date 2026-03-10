---
name: cloud-foundation-fabric
version: "1.0.0"
description: >
  MUST USE when building or modifying Google Cloud infrastructure with Cloud
  Foundation Fabric Terraform modules. Covers selecting CFF modules, wiring
  inputs and outputs, applying versioning and repository conventions, and
  composing Google Cloud architectures on top of Fabric. Do NOT use for generic
  Terraform work outside Cloud Foundation Fabric or for manual Google Cloud
  console setup unless the task explicitly depends on CFF.
metadata:
  source_url: https://github.com/GoogleCloudPlatform/cloud-foundation-fabric
  docs_url: https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/blob/master/README.md
  latest_version: v53.0.0
---

# Cloud Foundation Fabric (CFF)

## Overview

Cloud Foundation Fabric is a comprehensive suite of Terraform modules and end-to-end blueprints designed for Google Cloud Platform (GCP). It provides:

1. **Modules**: A library of composable, production-ready Terraform modules (e.g., `project`, `net-vpc`, `gke-cluster`)
2. **FAST**: An opinionated, stage-based landing zone toolkit for bootstrapping enterprise-grade GCP organizations

**Repository**: https://github.com/GoogleCloudPlatform/cloud-foundation-fabric  
**Latest Version**: `v53.0.0` (as of February 2025)

## Module Usage Pattern

**ALWAYS pin modules to a tagged release** to ensure stability:

```hcl
module "project" {
  source  = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/project?ref=v53.0.0"
  name    = "my-project"
  # ... other configuration
}
```

### Version Reference

| Version | Release Date | Status |
|---------|-------------|--------|
| v53.0.0 | 2025-02-12 | Latest |
| v52.1.0 | 2025-02-12 | Stable |
| v52.0.0 | 2025-01-31 | Stable |

## Quick Examples

### Project with APIs and IAM

```hcl
module "project" {
  source  = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/project?ref=v53.0.0"
  name    = "my-application"
  parent  = "folders/1234567890"
  
  services = [
    "compute.googleapis.com",
    "container.googleapis.com",
    "logging.googleapis.com",
  ]
  
  iam = {
    "roles/viewer" = ["group:developers@example.com"]
    "roles/editor" = ["serviceAccount:ci-cd@my-project.iam.gserviceaccount.com"]
  }
}
```

### VPC with Subnets

```hcl
module "vpc" {
  source  = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/net-vpc?ref=v53.0.0"
  project_id = module.project.project_id
  name    = "production-vpc"
  
  subnets = [
    {
      name          = "subnet-1"
      region        = "us-central1"
      ip_cidr_range = "10.0.0.0/24"
    },
    {
      name          = "subnet-2"
      region        = "europe-west1"
      ip_cidr_range = "10.0.1.0/24"
    }
  ]
}
```

### GKE Autopilot Cluster

```hcl
module "gke" {
  source  = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/gke-cluster-autopilot?ref=v53.0.0"
  project_id = module.project.project_id
  name    = "main-cluster"
  location = "us-central1"
  
  vpc_config = {
    network    = module.vpc.self_link
    subnetwork = module.vpc.subnet_self_links["us-central1/subnet-1"]
  }
}
```

## Reference Documentation

For detailed information, see the following reference guides:

- **[Module Catalog](./references/module-catalog.md)** - Complete list of all CFF modules organized by category
- **[Design Principles](./references/design-principles.md)** - The Zen of Fabric, common interfaces, and naming conventions
- **[Factory Patterns](./references/factory-patterns.md)** - Configuration-driven resource creation using YAML
- **[Cursed Knowledge](./references/cursed-knowledge.md)** - Edge cases, gotchas, and advanced patterns
- **[Configuration](./references/configuration.md)** - Tool setup, environment variables, and provider configuration

## Common Patterns

### IAM Interface

Most modules support consistent IAM patterns:

```hcl
iam = {
  "roles/viewer" = ["user:user@example.com"]
  "roles/editor" = ["group:group@example.com"]
}
```

### No Random Suffixes

Use explicit `prefix` instead of random suffixes:

```hcl
module "project" {
  source = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/project?ref=v53.0.0"
  name   = "application"
  prefix = "prod"  # Creates: prod-application
}
```

## Key Files

| File | Purpose |
|------|---------|
| [CURSED_KNOWLEDGE.md](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/blob/master/CURSED_KNOWLEDGE.md) | Edge cases and gotchas |
| [FACTORIES.md](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/blob/master/FACTORIES.md) | Factory patterns documentation |
| [CONTRIBUTING.md](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/blob/master/CONTRIBUTING.md) | Development guidelines |
| [GEMINI.md](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/blob/master/GEMINI.md) | AI assistant context |
| [CHANGELOG.md](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/blob/master/CHANGELOG.md) | Release history |

## External References

- **Repository**: https://github.com/GoogleCloudPlatform/cloud-foundation-fabric
- **Modules**: https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules
- **FAST Documentation**: https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/fast
- **Blueprints**: https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/blueprints
