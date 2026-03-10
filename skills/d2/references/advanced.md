---
name: d2-advanced
version: "1.0.0"
description: Complete reference for D2 advanced features including variables, globs, composition, imports, multi-board diagrams, and models.
metadata:
  source_url: https://d2lang.com/tour/vars
---

# D2 Advanced Features Reference

Complete reference for variables, globs, composition, imports, and other advanced D2 features.

---

**[Back to Main Documentation](../SKILL.md)** | [Shapes](../references/shapes.md) | [Sequence Diagrams](../references/sequence.md) | [Database & UML](../references/database.md) | [Examples](../references/examples.md)

## Variables and Substitutions

```d2
vars: {
  colors: {
    primary: "#3b82f6"
    secondary: "#10b981"
  }
  names: {
    service1: "Auth Service"
    service2: "User Service"
  }
}

service1: ${vars.names.service1} {
  style.fill: ${vars.colors.primary}
}
```

### Spread Substitutions

```d2
vars: {
  table_fields: {
    id: int {constraint: PK}
    last_updated: timestamp
  }
}

my_table: {
  shape: sql_table
  ...${vars.table_fields}
  name: string
}
```

### Configuration Variables

```d2
vars: {
  d2-config: {
    theme-id: 1
    pad: 10
    layout-engine: dagre
  }
}
```

### Single Quotes Bypass Substitutions

```d2
ab: 'Send field ${names}'  # Literal text, no substitution
```

## Globs

Apply styles globally:

```d2
# Apply to all shapes
**: {
  style.fill: "#f3f4f6"
}

# Filter by shape
*.shape: person

# Recursive globs
**: {
  style.stroke-width: 2
}

# Filters with &
bravo: {shape: person}
charlie: {shape: person}
*: &shape: person
  style.fill: blue

# Property filters
*: &connected: true
  style.stroke: red

*: &leaf: true
  style.fill: green

# Inverse filters
*: !&shape: person
  style.fill: gray

# Connection globs
* -> *
```

### Glob Connections

```d2
# Connect all to all
* -> *

# Self-connections are automatically omitted
```

### Scoped Globs

```d2
foods: {
  pizza: {
    cheese
    sausage
  }
  # Glob only applies within this scope
  *: {style.fill: orange}
}
```

### Global Globs (***)

```d2
# Applies globally including nested layers and across imports
***: {
  style.fill: "#f3f4f6"
}
```

## Composition (Layers, Scenarios, Steps)

```d2
direction: right

x -> y -> z

layers: {
  scenario1: {
    x -> y
  }
  scenario2: {
    x -> z
  }
}

scenarios: {
  error_case: {
    x.style.fill: red
  }
}

steps: {
  1: {
    x -> y
  }
  2: {
    y -> z
  }
}
```

### Board Types

- `layers` - New base (no inheritance)
- `scenarios` - Inherits from base layer
- `steps` - Inherits from previous step

## Legend

```d2
vars: {
  d2-legend: {
    # Legend automatically generated
  }
}

# Or rename legend
vars: {
  d2-legend: {
    label: 图例  # "Legend" in Chinese
  }
}
```

Hide shapes from legend by setting opacity:
```d2
api-1: {style.opacity: 0}
```

## Models (Suspend/Unsuspend)

Define models once, display in different ways:

```d2
# Define models
Restaurants: {
  Chipotle
  Chick-Fil-A
  BurgerKing
}

Diners: {
  daniel
  zack
}

# Relationships
Restaurants.Chipotle -> Diners.daniel: competes with
Diners.zack -> Restaurants.Chipotle: eat at

# Suspend all
**: {suspend: true}

# Unsuspend specific parts
Restaurants: {unsuspend: true}
Diners: {unsuspend: true}
Restaurants.Chipotle -> Diners.daniel: {unsuspend: true}
```

## Imports

### Regular Import

```d2
a: @x  # Imports x.d2 as a's value
```

### Spread Import

```d2
a: {
  ...@x  # Inserts x.d2 contents into a
}
```

### Partial Imports

```d2
# Import specific object from file
manager: @people.john
```

### Relative Imports

```d2
@./subdirectory/file
@../parent/file
```

## Comments

### Line Comments

```d2
# This is a comment
shape: rectangle  # inline comment
```

### Block Comments

```d2
"""
This is a
multiline comment
"""
```

## Overrides

Redeclaring merges with previous declaration:

```d2
Visual Studio Code: {
  label: VS Code
  style.fill: "#007ACC"
}

# Later override
Visual Studio Code: Text Editor
```

### Null to Delete

```d2
shape_to_remove: null
connection_to_remove: null
```

Implicit nulls: Nulling a shape with connections/descendants also nulls those.

## Strings

### Unquoted Strings

D2 favors unquoted strings for ease of use:

```d2
Philips: Switch
```

Leading and trailing whitespace is trimmed automatically.

**Forbidden characters** (require quotes): Special syntax characters used elsewhere in D2.

### Quoted Strings

Use single or double quotes when needed:

```d2
"$$$###"
'Special $tring'
```

Use double quotes if text contains single quotes, and vice versa. Escape with `\` if both are present.

### Block Strings

Use `|` for multiline content:

```d2
mytext: |md
  # I can do headers
  - lists
  - lists
  
  And other normal markdown stuff
|
```

Autoformat will correct indentation automatically.
