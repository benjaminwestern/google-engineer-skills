---
name: adk-go-patterns
version: "1.0.0"
description: Go patterns and code samples for Google ADK including agent structure, tool definitions, and launcher configuration.
metadata:
  source_url: https://github.com/google/adk-go
  docs_url: https://google.github.io/adk-docs/
---

# Go Patterns

## Installation

```bash
go get google.golang.org/adk
go get google.golang.org/genai
```

## Basic Agent Structure

```go
package main

import (
    "context"
    "log"
    
    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/launcher/web"
    "google.golang.org/adk/model/gemini"
    "google.golang.org/adk/tool"
    "google.golang.org/genai"
)

func main() {
    ctx := context.Background()
    
    // Create Gemini model
    model, err := gemini.NewModel(ctx, "gemini-2.5-flash", &genai.ClientConfig{})
    if err != nil {
        log.Fatal(err)
    }
    
    // Create agent
    agent, err := llmagent.New(llmagent.Config{
        Name:        "assistant",
        Model:       model,
        Instruction: "You are a helpful assistant.",
    })
    if err != nil {
        log.Fatal(err)
    }
    
    // Launch with web UI
    web.NewLauncher().Launch(ctx, agent)
}
```

## Agent Types

### LlmAgent

```go
import "google.golang.org/adk/agent/llmagent"

agent, _ := llmagent.New(llmagent.Config{
    Name:        "researcher",
    Model:       model,
    Instruction: "Research assistant that searches the web.",
    Description: "Web research agent",
    Tools:       []tool.Tool{searchTool},
})
```

### SequentialAgent

```go
import "google.golang.org/adk/agent/sequentialagent"

pipeline, _ := sequentialagent.New(sequentialagent.Config{
    Name:      "research_pipeline",
    SubAgents: []agent.Agent{researcher, summarizer, writer},
})
```

### ParallelAgent

```go
import "google.golang.org/adk/agent/parallelagent"

parallel, _ := parallelagent.New(parallelagent.Config{
    Name:      "multi_search",
    SubAgents: []agent.Agent{webSearcher, docSearcher},
})
```

### LoopAgent

```go
import "google.golang.org/adk/agent/loopagent"

loop, _ := loopagent.New(loopagent.Config{
    Name:          "refinement_loop",
    SubAgents:     []agent.Agent{writer, critic},
    MaxIterations: 3,
})
```

## Creating Tools

### Simple Function Tool

```go
package tools

import (
    "context"
    "google.golang.org/adk/tool"
)

// Define the function
func GetWeather(ctx context.Context, city string, units string) (map[string]interface{}, error) {
    // Implementation
    return map[string]interface{}{
        "temperature": 22,
        "conditions":  "sunny",
        "humidity":    45,
    }, nil
}

// Convert to tool
var WeatherTool = tool.FromFunction(GetWeather)
```

### Tool with Struct Definition

```go
package tools

import (
    "context"
    "fmt"
    "google.golang.org/adk/tool"
)

// Input struct
type WeatherInput struct {
    City  string `json:"city" description:"City name"`
    Units string `json:"units,omitempty" description:"Temperature units (celsius/fahrenheit)"`
}

// Output struct
type WeatherOutput struct {
    Temperature int    `json:"temperature"`
    Conditions  string `json:"conditions"`
    Humidity    int    `json:"humidity"`
}

func GetWeather(ctx context.Context, input *WeatherInput) (*WeatherOutput, error) {
    if input.Units == "" {
        input.Units = "celsius"
    }
    
    // Call weather API
    return &WeatherOutput{
        Temperature: 22,
        Conditions:  "sunny",
        Humidity:    45,
    }, nil
}

var WeatherTool = tool.FromFunction(GetWeather)
```

### Tool with ADC (BigQuery)

```go
package tools

import (
    "context"
    "fmt"
    "strings"
    
    "cloud.google.com/go/bigquery"
    "google.golang.org/adk/tool"
    "google.golang.org/adk/tool/toolcontext"
    "google.golang.org/api/option"
)

// BigQuery tool with ADC
type BigQueryInput struct {
    SQL       string `json:"sql" description:"SQL query to execute"`
    ProjectID string `json:"project_id" description:"GCP project ID"`
}

type BigQueryOutput struct {
    Rows      []map[string]interface{} `json:"rows"`
    TotalRows int                      `json:"total_rows"`
}

func QueryBigQuery(ctx context.Context, tc *toolcontext.ToolContext, input *BigQueryInput) (*BigQueryOutput, error) {
    // ADC automatically finds credentials in GCP environments
    client, err := bigquery.NewClient(ctx, input.ProjectID)
    if err != nil {
        return nil, fmt.Errorf("failed to create BigQuery client: %w", err)
    }
    defer client.Close()
    
    // Check access level from state
    accessLevel, _ := tc.State.GetString("user:access_level")
    if accessLevel == "read_only" && !strings.HasPrefix(strings.ToUpper(strings.TrimSpace(input.SQL)), "SELECT") {
        return nil, fmt.Errorf("read-only users can only execute SELECT queries")
    }
    
    query := client.Query(input.SQL)
    it, err := query.Read(ctx)
    if err != nil {
        return nil, err
    }
    
    var rows []map[string]interface{}
    for {
        var row []bigquery.Value
        err := it.Next(&row)
        if err == iterator.Done {
            break
        }
        if err != nil {
            return nil, err
        }
        
        // Convert to map
        rowMap := make(map[string]interface{})
        for i, col := range it.Schema {
            rowMap[col.Name] = row[i]
        }
        rows = append(rows, rowMap)
    }
    
    return &BigQueryOutput{
        Rows:      rows,
        TotalRows: len(rows),
    }, nil
}

var BigQueryTool = tool.FromFunction(QueryBigQuery)
```

## State Management

### Using ToolContext

```go
package tools

import (
    "context"
    "google.golang.org/adk/tool/toolcontext"
)

func AddToCart(ctx context.Context, tc *toolcontext.ToolContext, item string, quantity int) (map[string]interface{}, error) {
    // Get existing cart
    cart, err := tc.State.Get("cart")
    if err != nil || cart == nil {
        cart = []map[string]interface{}{}
    }
    
    cartSlice := cart.([]map[string]interface{})
    cartSlice = append(cartSlice, map[string]interface{}{
        "item":     item,
        "quantity": quantity,
    })
    
    // Update state
    if err := tc.State.Set("cart", cartSlice); err != nil {
        return nil, err
    }
    
    return map[string]interface{}{
        "status":    "added",
        "cart_size": len(cartSlice),
    }, nil
}
```

## Multi-Agent System

```go
package main

import (
    "context"
    "log"
    
    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/agent/parallelagent"
    "google.golang.org/adk/agent/sequentialagent"
    "google.golang.org/adk/launcher/web"
    "google.golang.org/adk/model/gemini"
    "google.golang.org/genai"
)

func main() {
    ctx := context.Background()
    model, _ := gemini.NewModel(ctx, "gemini-2.5-flash", &genai.ClientConfig{})
    
    // Create leaf agents
    webSearcher, _ := llmagent.New(llmagent.Config{
        Name:        "web_searcher",
        Model:       model,
        Instruction: "Search the web for information.",
    })
    
    docSearcher, _ := llmagent.New(llmagent.Config{
        Name:        "doc_searcher", 
        Model:       model,
        Instruction: "Search internal documentation.",
    })
    
    summarizer, _ := llmagent.New(llmagent.Config{
        Name:        "summarizer",
        Model:       model,
        Instruction: "Summarize research findings.",
    })
    
    // Parallel research
    parallelResearch, _ := parallelagent.New(parallelagent.Config{
        Name:      "parallel_research",
        SubAgents: []agent.Agent{webSearcher, docSearcher},
    })
    
    // Sequential pipeline
    pipeline, _ := sequentialagent.New(sequentialagent.Config{
        Name:      "research_pipeline",
        SubAgents: []agent.Agent{parallelResearch, summarizer},
    })
    
    // Launch
    web.NewLauncher().Launch(ctx, pipeline)
}
```

## Callbacks

### Before Tool Callback

```go
package main

import (
    "context"
    "fmt"
    
    "google.golang.org/adk/agent"
    "google.golang.org/adk/callback"
    "google.golang.org/adk/tool"
)

func beforeToolCallback(ctx context.Context, t tool.Tool, args map[string]interface{}, tc *callback.ToolContext) (map[string]interface{}, error) {
    // Check authentication
    authenticated, _ := tc.State.GetBool("user:authenticated")
    if !authenticated {
        return map[string]interface{}{
            "error": "Authentication required",
        }, nil
    }
    
    // Validate parameters
    if t.Name() == "delete_database" {
        role, _ := tc.State.GetString("user:role")
        if role != "admin" {
            return map[string]interface{}{
                "error": "Admin role required",
            }, nil
        }
    }
    
    // Return nil to proceed with tool execution
    return nil, nil
}

// Attach to agent
agent, _ := llmagent.New(llmagent.Config{
    Name:                "guarded_agent",
    Model:               model,
    Tools:               []tool.Tool{deleteTool},
    BeforeToolCallback:  beforeToolCallback,
})
```

## A2A Protocol

### Exposing an Agent (Go)

```go
package main

import (
    "context"
    "log"
    "strconv"
    
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/launcher/a2a"
    "google.golang.org/adk/launcher/web"
    "google.golang.org/adk/model/gemini"
    "google.golang.org/genai"
)

func main() {
    ctx := context.Background()
    port := 8001
    
    model, _ := gemini.NewModel(ctx, "gemini-2.0-flash", &genai.ClientConfig{})
    
    agent, _ := llmagent.New(llmagent.Config{
        Name:        "math_agent",
        Model:       model,
        Instruction: "You solve math problems.",
        Tools:       []tool.Tool{solveTool},
    })
    
    // Launch with A2A support
    webLauncher := web.NewLauncher(a2a.NewLauncher())
    webLauncher.Launch(ctx, agent,
        "a2a", "--a2a_agent_url", "http://localhost:"+strconv.Itoa(port),
        "--port", strconv.Itoa(port),
    )
}
```

### Consuming Remote Agent

```go
package main

import (
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/agent/remoteagent"
)

// Connect to remote A2A agent
remoteAgent, _ := remoteagent.NewA2A(remoteagent.A2AConfig{
    Name:            "math_agent",
    Description:     "Agent that solves math problems.",
    AgentCardSource: "http://localhost:8001",
})

// Use as sub-agent
rootAgent, _ := llmagent.New(llmagent.Config{
    Name:      "root_agent",
    Model:     model,
    SubAgents: []agent.Agent{remoteAgent},
})
```

## Testing

```go
package main

import (
    "context"
    "testing"
    
    "google.golang.org/adk/runner"
    "google.golang.org/genai"
)

func TestAgent(t *testing.T) {
    ctx := context.Background()
    
    // Create in-memory runner
    r := runner.NewInMemoryRunner(agent, "test_app")
    
    // Create session
    session, err := r.SessionService().CreateSession(ctx, "test_user", "test_app")
    if err != nil {
        t.Fatal(err)
    }
    
    // Create message
    content := &genai.Content{
        Role:  "user",
        Parts: []*genai.Part{{Text: "Hello"}},
    }
    
    // Run agent
    events := []runner.Event{}
    for event, err := range r.Run(ctx, "test_user", session.ID, content) {
        if err != nil {
            t.Fatal(err)
        }
        events = append(events, event)
    }
    
    // Assert results
    if len(events) == 0 {
        t.Fatal("No events received")
    }
    
    finalText := events[len(events)-1].Content.Parts[0].Text
    if !strings.Contains(strings.ToLower(finalText), "expected") {
        t.Errorf("Expected response to contain 'expected', got: %s", finalText)
    }
}
```

## Project Structure

```
my_agent/
├── main.go              # Entry point
├── agent/
│   └── agent.go         # Agent definitions
├── tools/
│   ├── weather.go       # Tool implementations
│   └── bigquery.go      # ADC-integrated tools
├── auth/
│   └── wif.go          # Workload Identity Federation
└── go.mod
```

## go.mod

```go
module my_agent

go 1.22

require (
    cloud.google.com/go/bigquery v1.59.1
    google.golang.org/adk v0.0.0
    google.golang.org/genai v0.0.0
)
```

## Best Practices

1. **Use ADC** - No keys in production, automatic in GCP
2. **Handle errors** - Always check errors from New* functions
3. **Close clients** - Defer Close() on BigQuery/storage clients
4. **Use contexts** - Pass ctx through all operations
5. **Define structs** - Use typed inputs/outputs for tools
6. **Validate in callbacks** - Use BeforeToolCallback for auth
7. **Use toolcontext** - Access state via ToolContext, not globals
