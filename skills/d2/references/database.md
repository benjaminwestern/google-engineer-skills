---
name: d2-database
version: "1.0.0"
description: Complete reference for D2 SQL tables, entity-relationship diagrams (ERDs), UML class diagrams, and constraints.
metadata:
  source_url: https://d2lang.com/tour/sql-tables
---

# D2 Database and UML Reference

Complete reference for SQL tables, entity-relationship diagrams (ERDs), and UML class diagrams.

---

**[Back to Main Documentation](../SKILL.md)** | [Shapes](../references/shapes.md) | [Sequence Diagrams](../references/sequence.md) | [Advanced Features](../references/advanced.md) | [Examples](../references/examples.md)

## SQL Tables

For entity-relationship diagrams:

```d2
costumes: {
  shape: sql_table
  id: int {constraint: PK}
  silliness: int
  monster: int
  last_updated: timestamp
}

monsters: {
  shape: sql_table
  id: int {constraint: PK}
  movie: string
  weight: int
  last_updated: timestamp
}

costumes.monster -> monsters.id: {constraint: FK}
```

### Constraint Shortcuts

- `PK` or `primary_key` → PK
- `FK` or `foreign_key` → FK
- `UNQ` or `unique` → UNQ

Multiple constraints: Use array `{constraint: [PK, UNQ]}`

## UML Classes

```d2
parser: {
  shape: class
  
  # Fields
  lookahead: []rune
  lookaheadPos: d2ast.Position
  
  # Methods (contain '(')
  peek(): (r rune, eof bool)
  rewind(): void
  commit(): void
}
```

### Visibility Prefixes

- `+` or none → public
- `-` → private
- `#` → protected

## Professional Database Schema Example

```d2
direction: right

classes: {
  professional-table: {
    shape: sql_table
    style.fill: "#9FA7D0"
    style.stroke: "#2A2A33"
  }
}

users: {
  class: professional-table
  id: int {constraint: PK}
  email: string {constraint: UNQ}
  name: string
  created_at: timestamp
}

posts: {
  class: professional-table
  id: int {constraint: PK}
  user_id: int {constraint: FK}
  title: string
  content: text
  published_at: timestamp
}

users.id -> posts.user_id: {style.stroke: "#00205C"}
```

## UML Class Diagram Example

```d2
classes: {
  professional-class: {
    shape: class
    style.fill: "#9FA7D0"
    style.stroke: "#2A2A33"
  }
}

User: {
  class: professional-class
  
  -id: int
  +name: string
  +email: string
  
  +login(): bool
  +logout(): void
}

Post: {
  class: professional-class
  
  -id: int
  +title: string
  +content: string
  
  +publish(): void
  +edit(): void
}

User -> Post: creates {style.stroke: "#00205C"}
```

## Crow's Foot Notation

For ERD relationships:

```d2
users: {
  shape: sql_table
  id: int {constraint: PK}
}

orders: {
  shape: sql_table
  id: int {constraint: PK}
  user_id: int
}

# One-to-many: user has many orders
users -> orders: {
  source-arrowhead: {
    shape: cf-one
  }
  target-arrowhead: {
    shape: cf-many
  }
}
```

**Crow's foot options:**
- `cf-one` - One
- `cf-one-required` - One (required)
- `cf-many` - Many
- `cf-many-required` - Many (required)
