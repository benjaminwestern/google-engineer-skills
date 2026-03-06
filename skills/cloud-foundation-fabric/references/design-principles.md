---
name: cff-design-principles
version: "1.0.0"
description: Cloud Foundation Fabric design principles including the Zen of Fabric, common interfaces, naming conventions, and style guide.
metadata:
  source_url: https://github.com/GoogleCloudPlatform/cloud-foundation-fabric
  docs_url: https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/blob/master/README.md
---

# Design Principles

Cloud Foundation Fabric design principles and patterns.

**[Back to Main Documentation](../SKILL.md)**

---

## The Zen of Fabric

- **Design for composition** - Support whole infrastructures
- **Encapsulate logical entities** - Match single functional units in modules
- **Adopt common interfaces** - Decrease cognitive overload with standard variable patterns
- **Write flat and concise code** - Easy to clone, evolve and troubleshoot
- **Don't aim at covering all use cases** - Make default ones simple, complex ones possible
- **Prefer code readability** - Achieve IaC as documentation
- **Don't be too opinionated** - Allow users to implement exact requirements
- **Avoid side effects** - Never rely on external tools

## Common Interfaces

CFF modules use consistent interfaces across related modules:

### IAM Interface

Available in most modules:

```hcl
iam = {
  "roles/viewer" = ["user:user@example.com"]
  "roles/editor" = ["group:group@example.com"]
}

iam_additive = {
  "roles/viewer" = ["serviceAccount:sa@project.iam.gserviceaccount.com"]
}

group_iam = {
  "group@example.com" = ["roles/editor"]
}
```

### Logging Sinks Interface

```hcl
logging_sinks = {
  bigquery = {
    name   = "audit-logs"
    type   = "bigquery"
    filter = "severity >= WARNING"
  }
}
```

### Organization Policies Interface

```hcl
policy_boolean = {
  "constraints/compute.disableGuestAttributesAccess" = true
}

policy_list = {
  "constraints/compute.trustedImageProjects" = {
    inherit_from_parent = false
    suggested_value = "projects/my-project"
    status = true
    values = ["projects/my-project"]
  }
}
```

## No Random Suffixes

CFF avoids random suffixes. Use explicit `prefix` variable:

```hcl
module "project" {
  source = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/project?ref=v53.0.0"
  name   = "application"
  prefix = "prod"  # Creates: prod-application
}
```
