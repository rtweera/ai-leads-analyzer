# Database Documentation

This document describes the database schema and structure for the AI Leads Analyzer application.

## Database Overview

The AI Leads Analyzer uses PostgreSQL as its primary data store. The database stores lead information, email metadata, and AI analysis results.

## Database Setup

### Connection

**Type:** PostgreSQL 12+

**Connection String Format:**
```
postgresql://[user[:password]@][host][:port][/database]
```

**Example:**
```
postgresql://ai_leads_user:password@localhost:5432/ai_leads_db
```

### Migration Tool

**Tool:** Alembic (Database migration tool)

**Location:** `alembic/` directory

## Database Schema

### Tables

#### 1. all_leads

Main table storing lead information and AI analysis results.

**Table Name:** `all_leads`

**Columns:**

| Column | Type | Nullable | Index | Default | Description |
|--------|------|----------|-------|---------|-------------|
| id | INTEGER | NO | PRIMARY KEY | Auto | Lead unique identifier |
| record_inserted_at | TIMESTAMP | NO | YES | NOW() | When record was created |
| event_happened_at | VARCHAR | YES | NO | NULL | When the lead event occurred |
| lead_first_name | VARCHAR | NO | NO | NULL | Lead's first name |
| lead_last_name | VARCHAR | NO | NO | NULL | Lead's last name |
| lead_email | VARCHAR | NO | NO | NULL | Lead's email address |
| lead_phone | VARCHAR | NO | NO | NULL | Lead's phone number |
| lead_job_role | VARCHAR | NO | NO | NULL | Lead's job title/role |
| lead_company | VARCHAR | NO | NO | NULL | Lead's company |
| lead_country | VARCHAR | NO | NO | NULL | Lead's country |
| lead_state | VARCHAR | YES | NO | NULL | Lead's state/province |
| lead_industry | VARCHAR | NO | NO | NULL | Industry type |
| can_help_comment | VARCHAR | NO | NO | NULL | Comment about how we can help |
| area_of_interest | VARCHAR | NO | NO | NULL | Area of interest (e.g., API, Integration) |
| description | VARCHAR | NO | NO | NULL | Lead description |
| is_about_ai | BOOLEAN | YES | NO | NULL | Whether lead is AI-related |
| ai_reason | VARCHAR | YES | NO | NULL | Reason for AI classification |
| geranimo_response | JSON | YES | NO | NULL | Response from Geranimo system |

### SQL Definition

```sql
CREATE TABLE all_leads (
    id SERIAL PRIMARY KEY,
    record_inserted_at TIMESTAMP NOT NULL DEFAULT NOW(),
    event_happened_at VARCHAR,
    lead_first_name VARCHAR NOT NULL,
    lead_last_name VARCHAR NOT NULL,
    lead_email VARCHAR NOT NULL,
    lead_phone VARCHAR NOT NULL,
    lead_job_role VARCHAR NOT NULL,
    lead_company VARCHAR NOT NULL,
    lead_country VARCHAR NOT NULL,
    lead_state VARCHAR,
    lead_industry VARCHAR NOT NULL,
    can_help_comment VARCHAR NOT NULL,
    area_of_interest VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    is_about_ai BOOLEAN,
    ai_reason VARCHAR,
    geranimo_response JSON
);

-- Create indexes for frequently queried columns
CREATE INDEX idx_all_leads_email ON all_leads(lead_email);
CREATE INDEX idx_all_leads_company ON all_leads(lead_company);
CREATE INDEX idx_all_leads_country ON all_leads(lead_country);
CREATE INDEX idx_all_leads_inserted_at ON all_leads(record_inserted_at);
CREATE INDEX idx_all_leads_ai ON all_leads(is_about_ai);
```

## Data Types

### PostgreSQL Data Types Used

| Type | Description | Examples |
|------|-------------|----------|
| SERIAL | Auto-incrementing integer | 1, 2, 3... |
| VARCHAR | Variable-length text | "John Doe", "john@example.com" |
| TIMESTAMP | Date and time | 2024-01-15 10:30:00 |
| BOOLEAN | True/False value | true, false |
| JSON | JSON document | {"key": "value"} |

## Constraints

### Primary Key

```sql
PRIMARY KEY (id)
```

Ensures each lead has a unique identifier.

### Not Null Constraints

The following columns are required:
- `record_inserted_at`
- `lead_first_name`
- `lead_last_name`
- `lead_email`
- `lead_phone`
- `lead_job_role`
- `lead_company`
- `lead_country`
- `lead_industry`
- `can_help_comment`
- `area_of_interest`
- `description`

### Optional Fields

The following columns can be NULL:
- `event_happened_at`
- `lead_state`
- `is_about_ai`
- `ai_reason`
- `geranimo_response`

## Indexes

Indexes improve query performance on frequently searched columns:

```sql
-- Email lookup
CREATE INDEX idx_all_leads_email ON all_leads(lead_email);

-- Company filtering
CREATE INDEX idx_all_leads_company ON all_leads(lead_company);

-- Geographic filtering
CREATE INDEX idx_all_leads_country ON all_leads(lead_country);

-- Time-based queries
CREATE INDEX idx_all_leads_inserted_at ON all_leads(record_inserted_at);

-- AI classification filtering
CREATE INDEX idx_all_leads_ai ON all_leads(is_about_ai);
```

## Common Queries

### Retrieve All Leads

```sql
SELECT * FROM all_leads
ORDER BY record_inserted_at DESC
LIMIT 10 OFFSET 0;
```

### Find Lead by Email

```sql
SELECT * FROM all_leads
WHERE lead_email = 'john@example.com';
```

### Get Leads by Company

```sql
SELECT * FROM all_leads
WHERE lead_company = 'WSO2'
ORDER BY record_inserted_at DESC;
```

### Count AI-Related Leads

```sql
SELECT COUNT(*) as ai_lead_count
FROM all_leads
WHERE is_about_ai = true;
```

### Get Leads by Country

```sql
SELECT lead_country, COUNT(*) as lead_count
FROM all_leads
GROUP BY lead_country
ORDER BY lead_count DESC;
```

### Find Leads by Date Range

```sql
SELECT * FROM all_leads
WHERE record_inserted_at 
  BETWEEN '2024-01-01'::timestamp AND '2024-01-31'::timestamp
ORDER BY record_inserted_at DESC;
```

### Get Recent AI Analysis

```sql
SELECT 
  id, lead_email, lead_company, 
  is_about_ai, ai_reason, record_inserted_at
FROM all_leads
WHERE ai_reason IS NOT NULL
ORDER BY record_inserted_at DESC
LIMIT 20;
```

## Database Migrations

### Running Migrations

```bash
# Show current revision
alembic current

# Upgrade to latest
alembic upgrade head

# Upgrade by specific steps
alembic upgrade +2

# Downgrade by steps
alembic downgrade -1

# Downgrade to specific revision
alembic downgrade abc123
```

### Creating a Migration

After modifying models, create a migration:

```bash
alembic revision --autogenerate -m "Add new column to leads"
```

Review generated migration in `alembic/versions/` before applying.

## Backup and Recovery

### Backup Database

```bash
pg_dump ai_leads_db > backup.sql
```

### Restore Database

```bash
psql ai_leads_db < backup.sql
```

### Full Backup with Compression

```bash
pg_dump ai_leads_db | gzip > backup.sql.gz

# Restore
gunzip -c backup.sql.gz | psql ai_leads_db
```

## Performance Tips

### Query Optimization

1. **Use WHERE clauses** to filter data early
2. **Use indexes** on frequently searched columns
3. **Avoid N+1 queries** using JOINs
4. **Use EXPLAIN** to analyze query plans

```sql
EXPLAIN SELECT * FROM all_leads WHERE lead_country = 'USA';
```

### Connection Pooling

Use SQLAlchemy connection pool for efficient resource management:

```python
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

### Monitoring

Monitor database performance:

```bash
# Connect to database
psql ai_leads_db

# Show table sizes
SELECT 
  schemaname, tablename, 
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) 
FROM pg_tables 
WHERE schemaname NOT IN ('pg_catalog', 'information_schema');

# Show slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC LIMIT 10;
```

## Security

### User Privileges

Create limited database user for application:

```sql
-- Create user
CREATE USER ai_leads_app WITH PASSWORD 'secure_password';

-- Grant privileges on specific table
GRANT SELECT, INSERT, UPDATE ON all_leads TO ai_leads_app;

-- Restrict privileges for sensitive operations
REVOKE DELETE ON all_leads FROM ai_leads_app;
```

### Connection Security

- Use SSL/TLS for remote connections
- Use parameterized queries to prevent SQL injection
- Validate all input data
- Encrypt sensitive data at rest

## Troubleshooting

### Connection Issues

```bash
# Test connection
psql -U user -d ai_leads_db -h localhost

# Check if PostgreSQL is running
sudo service postgresql status
```

### Permission Denied

```sql
-- Check current permissions
\dp all_leads

-- Grant missing permissions
GRANT SELECT ON all_leads TO ai_leads_app;
```

### Slow Queries

```sql
-- Analyze query execution
EXPLAIN ANALYZE SELECT * FROM all_leads WHERE lead_country = 'USA';

-- Create missing indexes if needed
CREATE INDEX idx_new ON all_leads(column_name);
```

## Database Maintenance

### Vacuum and Analyze

Regular maintenance improves performance:

```bash
# Connect to database
psql ai_leads_db

# Vacuum to reclaim space
VACUUM ANALYZE;
```

### Statistics

Update table statistics for query optimizer:

```sql
ANALYZE all_leads;
```

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy ORM Documentation](https://docs.sqlalchemy.org/en/20/orm/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
