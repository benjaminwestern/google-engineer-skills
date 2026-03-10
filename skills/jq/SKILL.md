---
name: jq
version: "1.0.0"
description: >
  MUST USE when parsing, filtering, querying, transforming, or validating JSON
  with jq. Covers extracting fields from API responses, reshaping JSON
  documents, filtering arrays and objects, building shell pipelines around JSON,
  and composing jq expressions. Do NOT use for YAML processing, SQL queries, or
  general text manipulation unless jq is explicitly part of the task.
metadata:
  source_url: https://github.com/jqlang/jq
  docs_url: https://jqlang.github.io/jq/manual/
---

# jq - JSON Processor

jq is a lightweight and flexible command-line JSON processor. It's like `sed` for JSON data - you can use it to slice, filter, map, and transform structured data.

## Quick Start

```bash
# Pretty-print JSON
cat data.json | jq '.'

# Extract a field
cat data.json | jq '.name'

# Filter an array
cat data.json | jq '.items[] | select(.price > 10)'

# Transform data structure
cat data.json | jq '{name: .firstName, age: .years}'
```

## Core Concepts

### Basic Filter: `.`

The simplest jq program is `.`, which passes input through unchanged (useful for pretty-printing).

```bash
echo '{"name":"John","age":30}' | jq '.'
```

### Object Identifier-Index: `.foo`, `.foo.bar`

Access object properties using dot notation.

```bash
# Extract single field
echo '{"name": "John", "age": 30}' | jq '.name'
# Output: "John"

# Access nested properties
echo '{"user": {"name": "John", "email": "john@example.com"}}' | jq '.user.email'
# Output: "john@example.com"
```

### Array Index: `.[0]`, `.[2]`, `.[-1]`

Access array elements by index (negative indices count from the end).

```bash
# Get first element
echo '["a", "b", "c"]' | jq '.[0]'
# Output: "a"

# Get last element
echo '["a", "b", "c"]' | jq '.[-1]'
# Output: "c"

# Get range of elements
echo '[1, 2, 3, 4, 5]' | jq '.[1:3]'
# Output: [2, 3]
```

### Array/Object Value Iterator: `.[]`

Iterate over all elements of an array or values of an object.

```bash
# Iterate array
echo '[1, 2, 3]' | jq '.[]'
# Output: 1, 2, 3 (each on new line)

# Iterate object values
echo '{"a": 1, "b": 2}' | jq '.[]'
# Output: 1, 2
```

### Pipe: `|`

Combine filters by piping output of one into the next.

```bash
# Get first item's name from array
echo '[{"name":"Alice"},{"name":"Bob"}]' | jq '.[0] | .name'
# Output: "Alice"
```

## Common Filters

### Select: `select(condition)`

Filter elements based on a condition.

```bash
# Filter objects where age > 25
echo '[{"name":"Alice","age":30},{"name":"Bob","age":20}]' | jq '.[] | select(.age > 25)'

# Select with multiple conditions
cat users.json | jq '.[] | select(.age > 18 and .active == true)'
```

### Keys: `keys`, `keys_unsorted`

Get keys of an object.

```bash
# Get sorted keys
echo '{"z": 1, "a": 2, "m": 3}' | jq 'keys'
# Output: ["a", "m", "z"]

# Get keys in original order
echo '{"z": 1, "a": 2}' | jq 'keys_unsorted'
```

### Length: `length`

Get length of string, array, or number of keys in object.

```bash
# Array length
echo '[1, 2, 3, 4]' | jq 'length'
# Output: 4

# String length
echo '"hello"' | jq 'length'
# Output: 5

# Object key count
echo '{"a": 1, "b": 2}' | jq 'length'
# Output: 2
```

### Type: `type`

Get the type of a value.

```bash
echo '{"name": "test", "count": 5}' | jq '.[] | type'
# Output: "string", "number"
```

### Contains: `contains(element)`

Check if an element is contained in the input.

```bash
echo '["foo", "bar"]' | jq 'contains(["bar"])'
# Output: true

echo '{"name": "foo", "value": 42}' | jq 'contains({"name": "foo"})'
```

### Has Key: `has(key)`

Check if object has a specific key.

```bash
# Check if has key
echo '{"name": "John", "age": 30}' | jq 'has("name")'
# Output: true

# Check in array for index
echo '["a", "b", "c"]' | jq 'has(2)'
# Output: true
```

## String Functions

```bash
# Convert to string
echo '{"num": 42}' | jq '.num | tostring'

# Split string
echo '"hello,world"' | jq 'split(",")'
# Output: ["hello", "world"]

# Join array into string
echo '["hello", "world"]' | jq 'join(" ")'
# Output: "hello world"

# Convert to upper/lower case
echo '"hello"' | jq 'ascii_upcase'
# Output: "HELLO"

echo '"WORLD"' | jq 'ascii_downcase'
# Output: "world"
```

## Array Functions

```bash
# Add all elements
echo '[1, 2, 3, 4]' | jq 'add'
# Output: 10

# Flatten nested arrays
echo '[[1, 2], [3, 4]]' | jq 'flatten'
# Output: [1, 2, 3, 4]

# Reverse array
echo '[1, 2, 3]' | jq 'reverse'
# Output: [3, 2, 1]

# Sort array
echo '[3, 1, 4, 1, 5]' | jq 'sort'
# Output: [1, 1, 3, 4, 5]

# Unique elements
echo '[1, 2, 2, 3, 3, 3]' | jq 'unique'
# Output: [1, 2, 3]

# Group by property
cat data.json | jq 'group_by(.category)'
```

## Object Construction

```bash
# Create new object with selected fields
echo '{"firstName": "John", "lastName": "Doe", "age": 30}' | jq '{name: .firstName, years: .age}'

# Merge objects
echo '{"a": 1}' | jq '. + {"b": 2}'
# Output: {"a": 1, "b": 2}

# Delete a key
echo '{"a": 1, "b": 2, "c": 3}' | jq 'del(.b)'
# Output: {"a": 1, "c": 3}

# Get entries as key-value pairs
echo '{"a": 1, "b": 2}' | jq 'to_entries'
# Output: [{"key":"a","value":1},{"key":"b","value":2}]

# Convert entries back to object
echo '[{"key":"a","value":1}]' | jq 'from_entries'
# Output: {"a": 1}
```

## API Response Examples

### GitHub API Example

```bash
# Get last 5 commits and extract messages
curl 'https://api.github.com/repos/jqlang/jq/commits?per_page=5' | jq '.[].commit.message'

# Get first commit with specific fields
curl 'https://api.github.com/repos/jqlang/jq/commits?per_page=5' | jq '.[0] | {message: .commit.message, name: .commit.committer.name}'

# Get all commits as array of objects
curl 'https://api.github.com/repos/jqlang/jq/commits?per_page=5' | jq '[.[] | {message: .commit.message, name: .commit.committer.name}]'
```

### Working with Arrays

```bash
# Extract unique source URLs from skill-lock.json
cat ~/.agents/.skill-lock.json | jq -r '.skills[].sourceUrl' | sort -u

# Count skills by source
cat ~/.agents/.skill-lock.json | jq -r '.skills[].source' | sort | uniq -c

# Get all skill names as array
cat ~/.agents/.skill-lock.json | jq '[.skills | keys[]]'
```

## Command Line Options

```bash
# Raw output (no quotes around strings)
jq -r '.name' data.json

# Sort keys in output
cat data.json | jq -S '.'

# Compact output (one line)
cat data.json | jq -c '.'

# Output null instead of errors
jq -n '...' < data.json

# Pass JSON as argument
jq --arg name "John" '{"name": $name}'

# Read file into variable
jq --rawfile content file.txt '{"data": $content}'

# Slurp multiple JSON inputs into array
cat *.json | jq -s '.'
```

## Advanced Examples

### Recursive Descent: `..`

Find all values recursively.

```bash
# Find all "name" fields at any depth
cat data.json | jq '.. | .name? // empty'
```

### Conditional Logic

```bash
# If-then-else
cat users.json | jq '.[] | if .age >= 18 then "adult" else "minor" end'

# Alternative operator
cat data.json | jq '.name // "unknown"'
```

### Regular Expressions

```bash
# Test if matches regex
cat data.json | jq '.email | test("@example\\.com$")'

# Capture groups
cat data.json | jq '.version | capture("(?<major>\\d+)\\.(?<minor>\\d+)")'

# Split with regex
echo '"a.b;c"' | jq 'split("[.;]"; "g")'
```

### Defining Variables

```bash
# Store value in variable
cat data.json | jq '. as $data | $data.name'

# Multiple variables
cat data.json | jq '.items | . as [$first, $second] | {first, second}'
```

## Tips and Best Practices

### Use raw output for strings

When extracting string values, use `-r` to avoid extra quotes:
```bash
# Bad - outputs: "value"
cat data.json | jq '.key'

# Good - outputs: value
cat data.json | jq -r '.key'
```

### Handle null values safely

```bash
# Use ? operator to suppress errors on null
cat data.json | jq '.possibly_missing_field?'

# Provide default value
cat data.json | jq '.field // "default"'
```

### Pretty-print complex output

```bash
# Always pipe through jq for readable JSON
curl -s https://api.example.com/data | jq '.'
```

### Combine with other tools

```bash
# Extract URLs and download
cat urls.json | jq -r '.[]' | xargs curl -O

# Filter and process with other tools
cat data.json | jq -r '.items[] | "\(.name),\(.value)"' | csvlook
```

## Installation

### macOS
```bash
brew install jq
```

### Ubuntu/Debian
```bash
sudo apt-get install jq
```

### Other
See https://jqlang.github.io/jq/download/

## Resources

- Manual: https://jqlang.github.io/jq/manual/
- Tutorial: https://jqlang.github.io/jq/tutorial/
- Playground: https://jqplay.org/
