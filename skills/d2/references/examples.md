---
name: d2-examples
version: "1.0.0"
description: Complete working examples for all D2 diagram types including sequence diagrams, architecture diagrams, ERDs, UML classes, and grid layouts.
metadata:
  source_url: https://d2lang.com
---

# D2 Examples Gallery

Complete working examples for all diagram types and use cases.

---

**[Back to Main Documentation](../SKILL.md)** | [Shapes](../references/shapes.md) | [Sequence Diagrams](../references/sequence.md) | [Database & UML](../references/database.md) | [Advanced Features](../references/advanced.md)

## Example 1: Simple Connection

```d2
direction: right

A -> B: Hello
B -> C: World
```

## Example 2: Container with Styling

```d2
direction: down

Frontend: {
  style: {
    fill: "#9FA7D0"
    stroke: "#2A2A33"
  }
  
  Login
  Dashboard
  Settings
}

Backend: {
  style: {
    fill: "#00A7E1"
    stroke: "#2A2A33"
  }
  
  API
  Auth
}

Frontend.Login -> Backend.Auth: authenticate {style.stroke: "#00205C"}
```

## Example 3: Sequence Diagram with Professional Styling

```d2
shape: sequence_diagram

direction: right

classes: {
  professional-person: {
    shape: person
    style.fill: "#66CAD8"
    style.stroke: "#2A2A33"
  }
  professional-service: {
    style.fill: "#9FA7D0"
    style.stroke: "#2A2A33"
  }
  professional-database: {
    shape: cylinder
    style.fill: "#E82370"
    style.stroke: "#2A2A33"
  }
}

User: {class: professional-person}
Frontend: {class: professional-service}
Backend: {class: professional-service}
Database: {class: professional-database}

User -> Frontend: Login request
Frontend -> Backend: POST /api/login
Backend -> Database: Verify credentials
Database --> Backend: User data
Backend --> Frontend: Auth token
Frontend --> User: Login success
```

## Example 4: Grid Layout

```d2
direction: down

grid-rows: 2
grid-columns: 3
grid-gap: 20

classes: {
  professional-primary: {
    style.fill: "#9FA7D0"
    style.stroke: "#2A2A33"
  }
}

A: {class: professional-primary}
B: {class: professional-primary}
C: {class: professional-primary}
D: {class: professional-primary}
E: {class: professional-primary}
F: {class: professional-primary}
```

## Example 5: UML Class Diagram

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

## Example 6: Complex Composition

```d2
direction: right

x -> y -> z

layers: {
  overview: {
    label: |md
      # System Overview
      High-level architecture
    |
  }
  
  detailed: {
    x: {
      style.fill: "#9FA7D0"
      a
      b
    }
    y: {
      style.fill: "#00A7E1"
      c
      d
    }
    z: {
      style.fill: "#E82370"
      e
    }
  }
}

scenarios: {
  normal: {
    x.style.fill: "#00CC40"
  }
  
  error: {
    y.style.fill: "#F22000"
    y.label: Error State
  }
}
```

## Example 7: Professional User Flow Diagram

```d2
direction: down

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
  professional-feature: {
    style.fill: "#00A7E1"
    style.stroke: "#2A2A33"
    style.stroke-width: 1
  }
}

User: {class: professional-person}

Authentication: {
  class: professional-service
  Login
  Logout
}

Features: {
  class: professional-feature
  Dashboard
  Profile
  Settings
}

User -> Authentication.Login: sign in {style.stroke: "#00205C"}
Authentication.Login -> Features.Dashboard: redirect {style.stroke: "#00205C"}
Features.Dashboard -> User: display {style.stroke: "#00205C"}
```

## Example 8: Professional System Architecture

```d2
direction: right

classes: {
  professional-person: {
    shape: person
    style.fill: "#66CAD8"
    style.stroke: "#2A2A33"
  }
  professional-service: {
    style.fill: "#9FA7D0"
    style.stroke: "#2A2A33"
  }
  professional-external: {
    shape: cloud
    style.fill: "#00A7E1"
    style.stroke: "#2A2A33"
  }
  professional-database: {
    shape: cylinder
    style.fill: "#E82370"
    style.stroke: "#2A2A33"
  }
}

Client: {class: professional-person}
LoadBalancer: {class: professional-service}
WebServer: {
  class: professional-service
  API1
  API2
}
Database: {class: professional-database}
Cache: {class: professional-database}
ExternalAPI: {class: professional-external}

Client -> LoadBalancer: HTTPS {style.stroke: "#00205C"}
LoadBalancer -> WebServer.API1: route {style.stroke: "#00205C"}
WebServer.API1 -> Database: query {style.stroke: "#00205C"}
WebServer.API1 -> Cache: get/set {style.stroke: "#00205C"}
WebServer.API1 -> ExternalAPI: fetch {style.stroke: "#00205C"}
```

## Example 9: Professional Database Schema

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

## Example 10: Multi-Agent System with Groups and Error Handling

Complete example showing proper group syntax, classes with labels, and quoted special characters:

```d2
shape: sequence_diagram

direction: right

classes: {
  user: {
    shape: person
    style.fill: "#66CAD8"
    style.stroke: "#2A2A33"
  }
  agent: {
    style.fill: "#9FA7D0"
    style.stroke: "#2A2A33"
  }
  external: {
    shape: cloud
    style.fill: "#00A7E1"
    style.stroke: "#2A2A33"
  }
}

User: {class: user}
Router: {class: agent; label: AGN-01 Router}
Intent: {class: agent; label: AGN-02 Intent}
Writer: {class: agent; label: AGN-03 Writer}
Executor: {class: agent; label: AGN-04 Executor}
BigQuery: {class: external; label: BigQuery MCP}

User -> Router: Natural language query
Router -> Router: Classify intent
Router -> Intent: Route to Intent Agent

Intent -> BigQuery: "SELECT * FROM tables"
BigQuery --> Intent: Schema metadata

Intent -> Writer: Contextualized intent
Writer -> Writer: Generate SQL with "TABLESAMPLE 1%"
Writer -> Executor: SQL query and context

Executor -> BigQuery: Execute dry-run
BigQuery --> Executor: Estimated bytes

group Validation Fails {
  Executor -> Writer: Return errors
  Writer -> Executor: Regenerated SQL
}

group Expensive Query {
  Executor -> User: Request confirmation
  User --> Executor: Approve
}

Executor -> BigQuery: Execute query
BigQuery --> Executor: Results and metadata
Executor --> User: Natural language response
```
