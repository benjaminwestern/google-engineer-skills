---
name: cff-cursed-knowledge
version: "1.0.0"
description: Critical edge cases, gotchas, and advanced patterns for Cloud Foundation Fabric including resource dependencies and lifecycle management.
metadata:
  source_url: https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/blob/master/CURSED_KNOWLEDGE.md
  docs_url: https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/blob/master/CURSED_KNOWLEDGE.md
---

# Cursed Knowledge

Critical edge cases, gotchas, and advanced patterns learned from building and using Cloud Foundation Fabric.

**[Back to Main Documentation](../SKILL.md)**

---

## Resource Dependencies

### Use `.id` Over `.name`

When referring to other resources, use `.id` instead of `.name`. The `.id` is computed and forces updates when the referred resource is replaced:

```hcl
# Good - forces recreate when subnet changes
resource "google_compute_instance" "vm" {
  depends_on = [google_compute_subnetwork.subnet]
  network_interface {
    subnetwork = google_compute_subnetwork.subnet.id
  }
}
```

## Create-Before-Destroy (CBD)

### CBD is Contagious

Resources depending on a CBD-marked resource also become CBD:

```hcl
# If instance_template has create_before_destroy = true
# then this subnetwork also becomes CBD
resource "google_compute_subnetwork" "subnet" {
  # ...
}
```

**Solution**: Change map keys to force independent operations:

```hcl
resource "google_compute_subnetwork" "subnet" {
  for_each = local.map
  # Changing the key makes operations independent
}
```

## Data Resources

### Avoid `data` Resources

Data resources can cause issues:
- When reading is deferred to apply, values become "known after apply"
- Can cause unnecessary resource replacement
- May require manual intervention if deployment fails mid-way

**Safe use cases**:
- Validating invariants (resource guaranteed to exist)
- Using outputs in attributes without `ForceNew` flag

## Type Checking

### Ternary Type Checking

Ternary expressions require identical types on both sides:

```hcl
# May fail - null and tonumber(null) don't converge
value = var.x ? tonumber(null) : null

# Use this instead for maps in for_each
local.partially_known == null ? [] : local.partially_known
# NOT: try(local.partially_known, [])  <- loses "known after apply" status
```

## ignore_changes

### Be Careful with `ignore_changes`

Terraform reads ignored values during plan and uses plan values during apply. If another resource touches the ignored argument, results may be incorrect.

**Don't mix**:
- `google_access_context_manager_service_perimeter` with `ignore_changes`
- `google_access_context_manager_service_perimeter_resource` in the same state

## Maps vs Lists

### Maps are Best for `for_each`

Using lists means inserting items causes replacement of subsequent resources:

```hcl
# Good - map preserves resource identity
resource "google_compute_subnetwork" "subnets" {
  for_each = {
    subnet-1 = { region = "us-central1", cidr = "10.0.0.0/24" }
    subnet-2 = { region = "us-central1", cidr = "10.0.1.0/24" }
  }
  # ...
}
```

## Empty Plans

### Always Run `terraform plan` After `apply`

A non-empty plan after apply indicates:
- Bug in Terraform code
- Provider issue
- Configuration not applied as expected

## Additional Resources

For more edge cases and detailed explanations, refer to the [official CURSED_KNOWLEDGE.md](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/blob/master/CURSED_KNOWLEDGE.md) in the CFF repository.
