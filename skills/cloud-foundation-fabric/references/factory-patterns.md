---
name: cff-factory-patterns
version: "1.0.0"
description: Factory patterns for Cloud Foundation Fabric including project factory, VPC factory, and YAML-driven resource creation.
metadata:
  source_url: https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/blob/master/FACTORIES.md
  docs_url: https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/blob/master/FACTORIES.md
---

# Factory Patterns

Factory patterns allow driving resource creation from YAML configuration files.

**[Back to Main Documentation](../SKILL.md)**

---

## Overview

Factories provide a declarative way to create multiple resources from YAML configuration files, enabling:
- Configuration-driven infrastructure
- GitOps workflows
- Environment-specific customizations
- Reduced Terraform code duplication

## Project Factory

Create multiple projects from YAML configurations:

```hcl
module "factory" {
  source  = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/project-factory?ref=v53.0.0"
  
  factories_config = {
    projects = {
      data_path = "projects/"
      rules_file = "rules.yaml"
    }
    folders = {
      data_path = "folders/"
    }
  }
  
  context = {
    organization_id = var.organization_id
    folder_id       = var.folder_id
  }
}
```

Example `projects/app1.yaml`:

```yaml
name: application-1
services:
  - compute.googleapis.com
  - storage.googleapis.com
iam:
  roles/editor:
    - group:developers@example.com
```

## VPC Factory

Create VPCs and subnets from YAML:

```hcl
module "vpc-factory" {
  source  = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/net-vpc-factory?ref=v53.0.0"
  
  factories_config = {
    vpcs = {
      data_path = "vpcs/"
    }
  }
  
  context = {
    project_id = var.project_id
  }
}
```

## Firewall Factory

Create firewall rules from YAML:

```hcl
module "firewall" {
  source  = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/net-vpc-firewall?ref=v53.0.0"
  project_id = var.project_id
  network   = module.vpc.name
  
  factories_config = {
    rules_folder = "firewall-rules/"
  }
}
```

## Factory Configuration Structure

### Projects Factory YAML Schema

```yaml
# Required
name: project-name

# Optional
services:
  - compute.googleapis.com
  - storage.googleapis.com

iam:
  roles/editor:
    - user:user@example.com
  roles/viewer:
    - group:developers@example.com

labels:
  environment: production
  team: platform

budget:
  amount: 1000
  alert_spent_percents: [50, 80, 100]
```

### VPC Factory YAML Schema

```yaml
# Required
name: vpc-name

# Optional
subnets:
  - name: subnet-1
    region: us-central1
    ip_cidr_range: 10.0.0.0/24
    private_ip_google_access: true
  
  - name: subnet-2
    region: europe-west1
    ip_cidr_range: 10.0.1.0/24

routes:
  - name: default-internet
    dest_range: 0.0.0.0/0
    next_hop_internet: true
```
