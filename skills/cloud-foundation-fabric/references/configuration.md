---
name: cff-configuration
version: "1.0.0"
description: Configuration reference for Cloud Foundation Fabric including mise setup, Terraform version compatibility, and environment variables.
metadata:
  source_url: https://github.com/GoogleCloudPlatform/cloud-foundation-fabric
  docs_url: https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/blob/master/README.md
---

# Configuration Reference

Tool configuration and environment setup for Cloud Foundation Fabric.

**[Back to Main Documentation](../SKILL.md)**

---

## Mise Configuration

When using [mise](https://mise.jdx.dev/) for tool management, configure Terraform version:

```toml
# ~/.config/mise/config.toml
[tools]
terraform = "1.10"

[env]
TF_PLUGIN_CACHE_DIR = "$HOME/.terraform.d/plugin-cache"
```

## Terraform Version Compatibility

| CFF Version | Terraform Version | Notes |
|-------------|-------------------|-------|
| v53.0.0+ | 1.10.x | Latest |
| v52.x | 1.9.x - 1.10.x | Stable |
| v51.x | 1.8.x - 1.9.x | Legacy |

## Environment Variables

Common environment variables for CFF development:

```bash
# Plugin caching (reduces init time)
export TF_PLUGIN_CACHE_DIR="$HOME/.terraform.d/plugin-cache"

# Parallelism (default: 10)
export TF_PARALLELISM=10

# Enable provider plugin cache
export TF_PLUGIN_CACHE_MAY_BREAK_DEPENDENCY_LOCK_FILE=true
```

## Backend Configuration

Example backend configuration for CFF projects:

```hcl
terraform {
  backend "gcs" {
    bucket = "my-terraform-state-bucket"
    prefix = "infrastructure/production"
  }
}
```

## Provider Configuration

Recommended Google provider configuration:

```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.0, < 7.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = ">= 5.0, < 7.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}
```
