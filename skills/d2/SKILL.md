---
name: d2
version: "1.1.0"
description: >
  MUST USE when creating or editing diagrams in D2. Covers sequence diagrams,
  flowcharts, architecture diagrams, ERDs, UML class diagrams, grid layouts,
  and other text-defined diagrams rendered with D2 syntax. Do NOT use for
  Mermaid, PlantUML, draw.io, or image-editing tasks unless the user explicitly
  wants D2 output.
metadata:
  source_url: https://github.com/terrastruct/d2
  docs_url: https://d2lang.com
---

# D2 Diagramming

Create professional diagrams using D2 (Declarative Diagramming) syntax. D2 generates clean, readable diagrams from text definitions.

## Installation

This skill requires the D2 CLI tool. We use **mise** to manage all tools.

### Using mise (Preferred)

Add to your `~/.config/mise/config.toml`:

```toml
[tools]
"go:oss.terrastruct.com/d2" = { version = "latest" }
```

Then install:

```bash
mise install

# Verify installation:
mise list | grep d2
```

### Alternative: Go Install

```bash
go install oss.terrastruct.com/d2@latest
```

## When to use me

Use this skill when you need to:
- Create sequence diagrams showing temporal flow between actors
- Generate flowcharts for process visualization
- Build architecture diagrams
- Create entity-relationship diagrams (ERDs)
- Visualize system interactions
- Design UML class diagrams
- Build grid-based diagrams
- Create multi-board compositions (layers, scenarios, steps)

## Quick Start

### Basic Connections

```d2
direction: right

A -> B: connection label
B -> C: another connection
```

**Connection types:**
- `--` - Line connection
- `->` - Arrow connection  
- `<-` - Reverse arrow connection
- `<->` - Bidirectional arrow connection

### Simple Shapes

```d2
imAShape
my_shape: Custom Label Here
PostgreSQL: {shape: cylinder}
User: {shape: person}
API: {shape: cloud}
```

## Professional Styling Standards

### Brand Colors

```json
{
  "Primary Blue": "#9FA7D0",
  "Light Blue": "#00A7E1",
  "Pink": "#E82370",
  "Teal": "#66CAD8",
  "Indigo": "#404FA2",
  "Green": "#00CC40",
  "Lime": "#CBDB2A",
  "Yellow": "#F9EB00",
  "Orange": "#FAA61A",
  "Red": "#F22000",
  "Dark Blue": "#00205C",
  "Slate": "#465669",
  "Black": "#000000",
  "Stroke": "#2A2A33"
}
```

### Reusable Classes

```d2
classes: {
  professional-person: {
    shape: person
    style.fill: "#66CAD8"
    style.stroke: "#2A2A33"
    style.stroke-width: 1
  }
  professional-service: {
    style.fill: "#9FA7D0"
    style.stroke: "#2A2A33"
    style.stroke-width: 1
  }
  professional-database: {
    shape: cylinder
    style.fill: "#E82370"
    style.stroke: "#2A2A33"
    style.stroke-width: 1
  }
  professional-external: {
    shape: cloud
    style.fill: "#00A7E1"
    style.stroke: "#2A2A33"
    style.stroke-width: 1
  }
}
```

## Common Patterns

### System Architecture

```d2
direction: right

classes: {
  service: {
    style.fill: "#9FA7D0"
    style.stroke: "#2A2A33"
  }
}

Client -> LoadBalancer: HTTPS
LoadBalancer -> API: route
API -> Database: query
```

### Sequence Diagram

```d2
shape: sequence_diagram

User -> Frontend: click button
Frontend -> Backend: POST /api/data
Backend --> Frontend: JSON response
Frontend --> User: display data
```

### Sequence Diagram with API Calls and SQL

```d2
shape: sequence_diagram

classes: {
  person: {shape: person}
  service: {}
  database: {shape: cylinder}
}

User: {class: person}
Frontend: {class: service}
Backend: {class: service}
Database: {class: database}

User -> Frontend: "Enter credentials"
Frontend -> Backend: "POST /api/auth/sync"
Backend -> Database: "SELECT id FROM users WHERE firebase_uid = ?"
Database --> Backend: "User record or null"
Backend --> Frontend: "Return user with NanoID"
```

## CLI Commands

### Generate outputs
```bash
# SVG (default)
d2 input.d2 output.svg

# PNG, PDF, PPTX
d2 input.d2 output.png
d2 input.d2 output.pdf

# Watch mode
d2 -w input.d2 output.svg

# Themes
d2 input.d2 output.svg --theme=1
d2 themes  # List themes
```

### Layout engines
```bash
d2 input.d2 output.svg --layout=dagre  # default
d2 input.d2 output.svg --layout=elk
d2 input.d2 output.svg --layout=tala
```

## Reference Documentation

For detailed information on specific topics, load the relevant reference:

| Reference | File | Contents |
|-----------|------|----------|
| Shapes & Styling | `references/shapes.md` | Complete shapes catalog, style keywords, arrowheads |
| Sequence Diagrams | `references/sequence.md` | Spans, groups, notes, self-messages |
| Database & UML | `references/database.md` | SQL tables, ERDs, UML classes, constraints |
| Advanced Features | `references/advanced.md` | Variables, globs, composition, imports, models |
| Examples Gallery | `references/examples.md` | Complete working examples for all diagram types |

**When to load references:**
- Creating complex diagrams with specialized shapes → Load `shapes.md`
- Building sequence diagrams with groups/spans → Load `sequence.md`
- Designing database schemas or UML → Load `database.md`
- Using variables, globs, or composition → Load `advanced.md`
- Need inspiration or templates → Load `examples.md`

## Best Practices

1. **Use classes for consistent styling** - Define reusable styles in `classes` block
2. **Quote JSON-like strings** - `{key: value}` should be `"{key: value}"`
3. **Keep labels concise** - Shorter is better for readability
4. **Group related components** - Use containers to organize complex diagrams
5. **Use block strings for multiline** - Use `|` followed by content and closing `|`
6. **Apply consistent styling** - Use the professional color palette
7. **Use vars for reusable values** - Define colors, names in vars section
8. **Leverage globs for global changes** - Apply styles to multiple shapes at once
9. **Quote labels with special characters** - Always wrap labels containing slashes, spaces, SQL, URLs, or `%` in double quotes: `BackendAPI -> Database: "SELECT * FROM users WHERE id = ?"`
10. **Classes and labels are separate** - Use `Node: {class: myclass; label: text}` syntax with semicolon separator
11. **Groups wrap connections, not define them** - Use `group name: { actor -> actor: message }` for grouping sequences

## Debugging

If D2 compilation fails:

1. **Check for unquoted JSON-like strings** - Wrap in quotes
2. **Ensure no trailing colons without values**
3. **Verify all shapes are properly closed**
4. **Block strings must be terminated** - Closing `|` on its own line
5. **Use double quotes for special characters** - `$`, `#`, `%`, etc.
6. **Check glob filter syntax** - Use `&` for filters, `!&` for inverse
7. **Quote connection labels with special characters** - Labels containing `/`, `?`, `=`, `%`, SQL keywords (SELECT, FROM, WHERE), or paths MUST be quoted:
   - ❌ `BackendAPI -> Database: GET /api/users?id=123`
   - ✅ `BackendAPI -> Database: "GET /api/users?id=123"`
   - ❌ `BackendAPI -> Database: SELECT * FROM users`
   - ✅ `BackendAPI -> Database: "SELECT * FROM users"`
   - ❌ `Backend -> DB: Sample 50% of data`
   - ✅ `Backend -> DB: "Sample 50% of data"`
8. **Cannot create edge inside edge** - In sequence diagrams with `group`, define the connections inside the group, don't nest groups within connection labels
9. **Invalid text beginning unquoted key** - When using semicolons in labels (e.g., `AGN-01; Router`), the parser may fail - use separate label field or quotes
