---
name: duckdb
description: >
  MUST USE when querying, transforming, or analysing local and embedded data
  with DuckDB. Covers SQL analytics over CSV, Parquet, and JSON files, data
  import and export workflows, ad hoc exploration, and embedded analytical
  database usage in scripts or pipelines. Do NOT use for transactional OLTP
  database design, external warehouse administration, or generic SQL work that
  does not specifically involve DuckDB.
---

# DuckDB

DuckDB is an in-process analytical database system designed for fast analytical queries. It supports SQL, embedded operation, and seamless integration with data science tools.

## Quick Start

```bash
# Install DuckDB CLI
curl https://install.duckdb.org | sh

# Start DuckDB shell
duckdb

# Run SQL query directly
duckdb -c "SELECT 42"

# Query a CSV file
duckdb -c "SELECT * FROM 'data.csv' LIMIT 10"
```

## Installation

### macOS/Linux
```bash
# Via install script
curl https://install.duckdb.org | sh

# Via Homebrew (macOS)
brew install duckdb

# Via conda
conda install -c conda-forge duckdb
```

### Python
```bash
pip install duckdb
```

### Other Platforms
- **Windows**: Download from https://duckdb.org/install/
- **R**: `install.packages("duckdb")`
- **Node.js**: `npm install duckdb`
- **Java**: Maven dependency `org.duckdb:duckdb_jdbc`

## SQL Statements

### SELECT
```sql
-- Basic query
SELECT * FROM users WHERE age > 25;

-- Aggregate
SELECT city, COUNT(*) FROM users GROUP BY city;

-- Join
SELECT a.*, b.name FROM orders a JOIN users b ON a.user_id = b.id;

-- FROM-first syntax (DuckDB extension)
FROM users SELECT * WHERE age > 25;
```

### CREATE TABLE
```sql
-- Create table with schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    age INTEGER,
    created_at TIMESTAMP
);

-- Create table from query
CREATE TABLE users AS SELECT * FROM 'users.csv';

-- Create table from CSV (shortcut)
CREATE TABLE users AS FROM 'users.csv';
```

### INSERT
```sql
-- Insert values
INSERT INTO users (id, name, age) VALUES (1, 'Alice', 30);

-- Insert from SELECT
INSERT INTO users SELECT * FROM new_users;

-- Insert from CSV
INSERT INTO users SELECT * FROM read_csv('new_users.csv');
```

### COPY (Import/Export)
```sql
-- Import CSV to table
COPY users FROM 'users.csv';

-- Import with options
COPY users FROM 'users.csv' (DELIMITER '|', HEADER true);

-- Import Parquet
COPY users FROM 'users.parquet' (FORMAT parquet);

-- Import JSON
COPY users FROM 'users.json' (FORMAT json, AUTO_DETECT true);

-- Export to CSV
COPY users TO 'users.csv' (FORMAT csv, HEADER);

-- Export query result
COPY (SELECT * FROM users WHERE age > 25) TO 'adults.parquet' (FORMAT parquet, COMPRESSION zstd);

-- Copy entire database
COPY FROM DATABASE db1 TO db2;
```

## Data Types

### General-Purpose Types
| Type | Aliases | Description |
|------|---------|-------------|
| `BOOLEAN` | BOOL, LOGICAL | True/false |
| `INTEGER` | INT4, INT, SIGNED | 4-byte integer |
| `BIGINT` | INT8, LONG | 8-byte integer |
| `HUGEINT` | - | 16-byte integer |
| `FLOAT` | FLOAT4, REAL | 4-byte float |
| `DOUBLE` | FLOAT8 | 8-byte float |
| `DECIMAL(p,s)` | NUMERIC(p,s) | Fixed precision |
| `VARCHAR` | CHAR, TEXT, STRING | Variable-length string |
| `DATE` | - | Calendar date |
| `TIME` | - | Time of day |
| `TIMESTAMP` | DATETIME | Date + time |
| `TIMESTAMPTZ` | - | Timestamp with timezone |
| `INTERVAL` | - | Time delta |
| `BLOB` | BYTEA, BINARY | Binary data |
| `JSON` | - | JSON object (requires json extension) |
| `UUID` | - | UUID data type |

### Nested Types
```sql
-- ARRAY (fixed-length)
SELECT ARRAY[1, 2, 3];
CREATE TABLE t (arr INTEGER[3]);

-- LIST (variable-length)
SELECT [1, 2, 3];
CREATE TABLE t (lst INTEGER[]);

-- STRUCT
SELECT {'x': 1, 'y': 2};
CREATE TABLE t (s STRUCT(x INTEGER, y INTEGER));

-- MAP
SELECT MAP([1, 2], ['a', 'b']);
CREATE TABLE t (m MAP(INTEGER, VARCHAR));

-- UNION
CREATE TABLE t (u UNION(int_type INTEGER, str_type VARCHAR));
```

## CSV Operations

### Read CSV
```sql
-- Auto-detect options
SELECT * FROM 'data.csv';

-- With explicit options
SELECT * FROM read_csv('data.csv', 
    delim = ',',
    header = true,
    columns = {
        'id': 'INTEGER',
        'name': 'VARCHAR'
    }
);

-- From stdin
cat data.csv | duckdb -c "SELECT * FROM read_csv('/dev/stdin')"
```

### CSV Options
| Option | Description | Default |
|--------|-------------|---------|
| `delim` / `sep` | Column delimiter | `,` |
| `header` | First line is header | `false` |
| `auto_detect` | Auto-detect format | `true` |
| `compression` | Compression type (gzip, zstd) | auto |
| `quote` | Quote character | `"` |
| `escape` | Escape character | `"` |
| `dateformat` | Date format string | - |
| `nullstr` | NULL representation | empty |
| `encoding` | File encoding | utf-8 |

## Parquet Operations

```sql
-- Read Parquet
SELECT * FROM 'data.parquet';

-- With options
SELECT * FROM read_parquet('data.parquet', hive_partitioning = true);

-- Write Parquet
COPY users TO 'users.parquet' (FORMAT parquet);

-- With compression
COPY users TO 'users.parquet' (FORMAT parquet, COMPRESSION zstd);
```

## Python API

```python
import duckdb

# Connect to database (in-memory)
con = duckdb.connect()

# Connect to file
con = duckdb.connect('mydb.db')

# Execute SQL
con.execute("CREATE TABLE users (id INTEGER, name VARCHAR)")
con.execute("INSERT INTO users VALUES (1, 'Alice')")

# Query and fetch
result = con.execute("SELECT * FROM users").fetchall()
print(result)  # [(1, 'Alice')]

# Fetch as DataFrame
df = con.execute("SELECT * FROM users").fetchdf()

# Query CSV directly
df = con.execute("SELECT * FROM 'data.csv'").fetchdf()

# Register DataFrame as table
con.register('my_df', df)
con.execute("SELECT * FROM my_df WHERE age > 25")

# Close connection
con.close()
```

## CLI Usage

```bash
# Start interactive shell
duckdb

# Run SQL file
duckdb < script.sql

# Execute command
duckdb -c "SELECT 42"

# Open database file
duckdb mydb.db

# Import CSV and query
duckdb -c "SELECT * FROM read_csv_auto('data.csv') LIMIT 10"

# Output formats
.duckdb -c "SELECT * FROM users" -csv    # CSV output
.duckdb -c "SELECT * FROM users" -json   # JSON output
```

## Common Workflows

### Import CSV to Table
```sql
-- Method 1: Direct CREATE TABLE AS
CREATE TABLE users AS SELECT * FROM 'users.csv';

-- Method 2: Pre-create table, then COPY
CREATE TABLE users (id INTEGER, name VARCHAR, age INTEGER);
COPY users FROM 'users.csv' (HEADER);

-- Method 3: With explicit column mapping
COPY users FROM 'users.csv' ( 
    HEADER,
    COLUMNS = {'id': 'INTEGER', 'name': 'VARCHAR', 'age': 'INTEGER'}
);
```

### Export Query Results
```sql
-- To CSV
COPY (SELECT * FROM users WHERE active = true) TO 'active_users.csv' (HEADER);

-- To Parquet
COPY (SELECT * FROM orders) TO 'orders.parquet' (FORMAT parquet);

-- To JSON
COPY (SELECT * FROM events) TO 'events.json' (FORMAT json);
```

### Working with Multiple Files
```sql
-- Query multiple CSV files
SELECT * FROM read_csv_auto('data/*.csv');

-- With filename column
SELECT filename, * FROM read_csv_auto('data/*.csv');

-- Hive partitioning
SELECT * FROM read_parquet('data/*/*/*.parquet', hive_partitioning = true);
```

## Extensions

```sql
-- Install and load extensions
INSTALL httpfs;
LOAD httpfs;

-- Popular extensions
INSTALL json;      LOAD json;      -- JSON support
INSTALL parquet;   LOAD parquet;   -- Parquet support
INSTALL httpfs;    LOAD httpfs;    -- HTTP/S3 support
INSTALL iceberg;   LOAD iceberg;   -- Apache Iceberg
INSTALL delta;     LOAD delta;     -- Delta Lake
INSTALL spatial;   LOAD spatial;   -- Geospatial data
```

## Tips

- **Auto-detection**: DuckDB's CSV sniffer automatically detects delimiters, headers, and types. Use `AUTO_DETECT = true`.
- **FROM-first syntax**: DuckDB allows `FROM table SELECT *` instead of `SELECT * FROM table`.
- **String literals**: Single quotes for strings `'text'`, double quotes for identifiers `"column"`.
- **In-process**: DuckDB runs embedded in your application - no server to manage.
- **Zero-copy**: Query Parquet and CSV files without loading them fully into memory.
- **Parallel CSV**: DuckDB automatically parallelizes CSV reading when possible.

## Resources

- Documentation: https://duckdb.org/docs/
- Live Demo: https://shell.duckdb.org
- GitHub: https://github.com/duckdb/duckdb
