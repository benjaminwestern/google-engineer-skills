---
name: terraform-testing-frameworks
version: "1.0.0"
description: Testing frameworks for Terraform including native tests, Terratest, decision flowcharts, mocking, and cost management strategies.
metadata:
  source_url: https://developer.hashicorp.com/terraform/docs
  docs_url: https://developer.hashicorp.com/terraform/docs
---

# Testing Frameworks

> **Part of:** [terraform-skill](../SKILL.md)
> **Purpose:** Testing strategy decisions for Terraform

This document helps you choose the right testing approach. For command reference, see [quick-reference.md](quick-reference.md#command-cheat-sheet).

---

## Testing Decision Flowchart

```bash
What do you need to test?
│
├─ Just syntax/format?
│  └─ terraform validate + fmt
│     See: [quick-reference.md](quick-reference.md)
│
├─ Static security scan?
│  └─ trivy + checkov
│     See: [security-compliance.md](security-compliance.md)
│
├─ Terraform 1.6+?
│  ├─ Simple logic/validation? → Native tests
│  └─ Complex integration? → Terratest
│
└─ Pre-1.6?
   └─ Terratest (or upgrade)
```

---

## Decision: Native Tests vs Terratest

| Factor | Native Tests | Terratest |
|--------|--------------|-----------|
| **Language** | HCL | Go |
| **Team requirement** | HCL knowledge | Go knowledge |
| **Dependencies** | None | Go toolchain |
| **Speed** | Fast (with mocks) | Slower (real infra) |
| **Ecosystem** | Growing | Mature, large community |
| **Best for** | Logic validation, unit tests | Integration, multi-provider |

**Decision rule:**

- Team uses HCL only → Native tests
- Team knows Go OR complex integration needed → Terratest
- Terraform < 1.6 → Terratest (native tests unavailable)

---

## Native Terraform Tests

**Available:** Terraform 1.6+

### Critical Decision: Plan vs Apply

This is the most important testing decision. Choose wrong and tests will fail.

| Mode | Use When | Speed |
|------|----------|-------|
| **`command = plan`** | Checking inputs, validating resource creation | Fast |
| **`command = apply`** | Checking computed values, accessing set-type blocks | Slower |

**Decision flowchart:**

```bash
What are you checking?
│
├─ Input values? → command = plan
├─ Computed values (IDs, ARNs)? → command = apply
└─ Set-type blocks? → command = apply
```

### Common Pattern: Plan for Inputs, Apply for Outputs

```hcl
# Test 1: Validate input (fast, plan mode)
run "validate_bucket_name" {
  command = plan
  
  variables {
    bucket_name = "my-test-bucket"
  }
  
  assert {
    condition     = google_storage_bucket.this.name == "my-test-bucket"
    error_message = "Bucket name should match input"
  }
}

# Test 2: Verify computed values (apply mode)
run "verify_bucket_url" {
  command = apply
  
  assert {
    condition     = startswith(google_storage_bucket.this.url, "gs://")
    error_message = "Bucket URL should start with gs://"
  }
}
```

### Working with Set-Type Blocks

**Problem:** Cannot index sets with `[0]`

```hcl
# ❌ WRONG - Will fail
condition = google_storage_bucket.this.lifecycle_rule[0].action[0].type == "Delete"

# ✅ CORRECT - Use apply mode + for expressions
run "test_lifecycle" {
  command = apply
  
  assert {
    condition = length([
      for rule in google_storage_bucket.this.lifecycle_rule :
      rule.action if rule.action[0].type == "Delete"
    ]) > 0
    error_message = "Delete action should be configured"
  }
}
```

### Decision: To Mock or Not?

| Approach | Speed | Realism | Best For |
|----------|-------|---------|----------|
| **With mocks** | Fast | Lower | Unit tests, logic validation |
| **Without mocks** | Slow | High | Integration tests, final validation |

```hcl
# With mocking (1.7+) - fast, no real resources
mock_provider "google" {}

run "test_logic" {
  command = plan
  # Tests run quickly without creating resources
}
```

---

## Terratest

**Best for:** Teams with Go experience, complex integration testing

### Critical Patterns

| Pattern | Why It Matters |
|---------|----------------|
| `t.Parallel()` | Enables parallel execution (faster) |
| `defer terraform.Destroy()` | Prevents orphaned resources |
| Unique identifiers | Prevents naming collisions |
| Resource tags | Enables cost tracking and cleanup |

```go
func TestStorageModule(t *testing.T) {
    t.Parallel()  // Always include
    
    terraformOptions := &terraform.Options{
        TerraformDir: "../examples/complete",
        Vars: map[string]interface{}{
            "bucket_name": "test-bucket-" + random.UniqueId(),
        },
    }
    
    defer terraform.Destroy(t, terraformOptions)  // Always include
    terraform.InitAndApply(t, terraformOptions)
    
    // Assertions here
    assert.NotEmpty(t, terraform.Output(t, terraformOptions, "bucket_name"))
}
```

### Decision: Test Stages

Use stages during development to skip slow steps:

```go
stage := test_structure.RunTestStage

stage(t, "setup", func() {
    terraform.InitAndApply(t, opts)
})

stage(t, "validate", func() {
    // Assertions
})

// Skip during iteration:
// export SKIP_setup=true
// export SKIP_teardown=true
```

### Cost Management Decisions

| Strategy | Implementation |
|----------|----------------|
| Use mocks | Native tests with `mock_provider` |
| TTL tags | Add labels with expiration |
| Main branch only | `if: github.ref == 'refs/heads/main'` |
| Smaller instances | `machine_type = "e2-micro"` in tests |

---

## Testing Checklist

Before considering a module tested:

- [ ] **Static analysis passes** (`fmt`, `validate`, `tflint`)
- [ ] **Security scan passes** (`trivy`, `checkov`)
- [ ] **Input validation works** - Invalid values rejected
- [ ] **Idempotency verified** - Second apply shows "No changes"
- [ ] **Cleanup verified** - `destroy` removes all resources

---

**Back to:** [Main Skill File](../SKILL.md)
