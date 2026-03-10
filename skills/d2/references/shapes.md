---
name: d2-shapes
version: "1.0.0"
description: Complete reference for D2 shapes catalog, styling options, visual customization, arrowheads, and style keywords.
metadata:
  source_url: https://d2lang.com/tour/shapes
---

# D2 Shapes and Styling Reference

Complete reference for shapes, styling options, and visual customization.

---

**[Back to Main Documentation](../SKILL.md)** | [Sequence Diagrams](../references/sequence.md) | [Database & UML](../references/database.md) | [Advanced Features](../references/advanced.md) | [Examples](../references/examples.md)

## Shapes Catalog

| Shape | Description | Use Case |
|-------|-------------|----------|
| `rectangle` | Default shape | General purpose |
| `square` | 1:1 aspect ratio | Equal dimensions |
| `page` | Page-like | Documents |
| `parallelogram` | Slanted rectangle | Data/process |
| `document` | Document with fold | Files |
| `cylinder` | Database symbol | Databases |
| `queue` | Queue shape | Message queues |
| `package` | Folder-like | Packages/modules |
| `step` | Process step | Workflows |
| `callout` | Speech bubble | Annotations |
| `stored_data` | Storage symbol | Data storage |
| `person` | Person icon | Users/actors |
| `diamond` | Decision point | Decisions |
| `oval` | Oval shape | States |
| `circle` | 1:1 circle | Points/conditions |
| `hexagon` | Hexagonal | Special nodes |
| `cloud` | Cloud icon | External services |
| `text` | Plain text | Labels only |
| `image` | Image/icon | Icons |
| `sql_table` | Database table | ERDs |
| `class` | UML class | UML diagrams |
| `sequence_diagram` | Sequence diagram | Temporal flows |

**Example:**
```d2
PostgreSQL: {shape: cylinder}
User: {shape: person}
API: {shape: cloud}
```

## Style Keywords

```d2
myshape: {
  style: {
    opacity: 0.5           # 0-1
    stroke: "#000"         # CSS color, hex, or gradient
    fill: "#fff"           # CSS color, hex, or gradient
    fill-pattern: dots     # dots, lines, grain, none
    stroke-width: 2        # 1-15
    stroke-dash: 5         # 0-10
    border-radius: 5       # 0-20
    shadow: true           # true/false
    3d: true              # true/false (rectangle/square only)
    multiple: true        # true/false
    double-border: true   # true/false (rectangles/ovals)
    font: mono            # mono
    font-size: 14         # 8-100
    font-color: "#333"    # CSS color
    animated: true        # true/false
    bold: true           # true/false
    italic: true         # true/false
    underline: true      # true/false
    text-transform: uppercase  # uppercase, lowercase, title, none
  }
}
```

**Root-level styles:**
```d2
style: {
  fill: "#f9fafb"        # Background color
  fill-pattern: dots
  stroke: "#000"         # Frame around diagram
  stroke-width: 2
  stroke-dash: 5
  double-border: true
}
```

## Arrowheads

```d2
x -> y: {
  source-arrowhead: {
    shape: circle
    style.filled: true
  }
  target-arrowhead: {
    shape: diamond
    style.filled: false
  }
}
```

**Arrowhead options:**
- `triangle` (default) - Use `style.filled: false` for hollow
- `arrow` - Pointier than triangle
- `diamond` - Use `style.filled: true`
- `circle` - Use `style.filled: true`
- `box` - Use `style.filled: true`
- `cf-one`, `cf-one-required` - Crow's foot notation
- `cf-many`, `cf-many-required` - Crow's foot notation
- `cross`

## Groups and Containers

```d2
direction: down

Frontend: {
  label: Frontend Layer
  style.fill: "#f3f4f6"
  
  LoginView: Login
  Dashboard: Dashboard
}

Backend: {
  label: Backend Layer
  style.fill: "#f3f4f6"
  
  AuthController
  UserController
}

Frontend.LoginView -> Backend.AuthController: authenticate
```

**Nested syntax:**
```d2
cloud: {
  gcp: {
    load_balancer
    api
    db
  }
  azure: {
    auth
    db
  }
}
```

**Reference parent:**
```d2
christmas: {
  presents
  birthdays: {
    presents
    _.presents: regift  # Refers to christmas.presents
  }
}
```

## Grid Diagrams

Use `grid-rows` and `grid-columns` for grid layouts:

```d2
direction: down

grid-rows: 2
grid-columns: 3

Executive
Legislative
Judicial
The American Government
Voters
Non-voters
```

**Grid keywords:**
- `grid-rows` - Number of rows
- `grid-columns` - Number of columns
- `vertical-gap` - Vertical gap size
- `horizontal-gap` - Horizontal gap size
- `grid-gap` - Sets both gaps
- `width` / `height` - Cell dimensions

**Dominant direction**: The first defined (rows or columns) determines fill order.

## Text and Code

**Markdown text:**
```d2
mytext: |md
  # I can do headers
  - lists
  - lists
  
  And other normal markdown stuff
|
```

**Code blocks:**
```d2
mycode: |go
  ctx := context.Background()
  client, err := storage.NewClient(ctx)
|
```

**LaTeX:**
```d2
math: |latex
  \lim_{h \to 0} \frac{f(x+h)-f(x)}{h}
|
```

**Non-Markdown text:**
```d2
mytext: {
  shape: text
  label: Plain text without Markdown
}
```

## Icons and Images

```d2
server: {
  icon: https://icons.terrastruct.com/gcp/Compute/Compute_Engine.svg
}

# Standalone icon shape
github: {
  shape: image
  icon: https://icons.terrastruct.com/dev/github.svg
}

# Local images
mycat: {
  icon: ./my_cat.png
}
```

Icons are automatically positioned. Use `near` keyword for positioning.

## Direction

```d2
direction: right  # up, down, right, left
```

**Directions per container (TALA only):**
```d2
container: {
  direction: down
  a -> b -> c
}
```

## Layouts

**Layout engines:**
- `dagre` (default) - Fast, layered/hierarchical layouts
- `elk` - More mature, better maintained, academic research-based
- `tala` - Terrastruct's custom engine, best for software architecture

```bash
# Specify layout
d2 input.d2 output.svg --layout=dagre

# Or environment variable
D2_LAYOUT=dagre d2 input.d2 output.svg
```

**Layout-specific features:**
- `near` set to another object (TALA only)
- `width` and `height` on containers (ELK only)
- `top` and `left` to lock positions (TALA only)
- Connections from ancestors to descendants (does not work in Dagre)
