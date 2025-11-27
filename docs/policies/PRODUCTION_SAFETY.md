# Production Safety Policy

## 🚨 PRODUCTION-SAFE RULES

### Data Protection Mandate

**NEVER** perform operations that could cause data loss:

**Forbidden actions:**
- ❌ Delete tables
- ❌ Truncate production data
- ❌ Rebuild schemas
- ❌ Modify schema outside migrations
- ❌ Assume missing data

If an operation could cause data loss → **STOP**.

### Database Operations Safety

#### Forbidden Operations
```bash
# ❌ FORBIDDEN - Production data destruction
DROP TABLE users;                    # Never delete production tables
TRUNCATE TABLE user_sessions;        # Never clear production data
DELETE FROM important_data;          # Never bulk delete without conditions

# ❌ FORBIDDEN - Schema modifications
ALTER TABLE users DROP COLUMN email;  # Use migration scripts instead
CREATE INDEX WITHOUT VALIDATION;      # Always validate schema changes
```

#### Allowed Operations (With Safeguards)
```bash
# ✅ ALLOWED - With proper investigation and backup
-- Read operations (always safe)
SELECT COUNT(*) FROM users;

-- Conditional deletes with investigation
DELETE FROM temp_sessions WHERE expired_at < NOW();

-- Development/Testing table operations
DROP TABLE test_feature_experiment;   # Clearly marked as test
TRUNCATE staging_import_data;         # Staging environment only
```

### Database Investigation Protocol

#### Before Any Destructive Operation
1. **Verify Environment**: Confirm you're not in production
2. **Check Table Purpose**: Understand what data the table contains
3. **Verify Backup**: Ensure recent backup exists
4. **Test in Development**: Validate operation in non-production environment
5. **Document Reason**: Record why operation is necessary

#### Investigation Commands
```bash
# Check if table contains production data
docker exec todowrite-postgres psql -U mcp_user -d todowrite -c "
SELECT
    schemaname,
    tablename,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes
FROM pg_stat_user_tables
WHERE tablename = 'your_table_name';
"

# Check recent activity
docker exec todowrite-postgres psql -U mcp_user -d todowrite -c "
SELECT schemaname, tablename, seq_scan, seq_tup_read
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY seq_tup_read DESC;
"

# Verify table structure and dependencies
docker exec todowrite-postgres psql -U mcp_user -d todowrite -c "
SELECT
    tc.table_name,
    tc.constraint_name,
    tc.constraint_type,
    kcu.column_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
WHERE tc.table_name = 'your_table_name';
"
```

### Environment Identification

#### Production Environment Indicators
```bash
# Check environment variables
echo $DATABASE_URL | grep -i prod
echo $APP_ENV | grep -i production

# Check database connection details
docker exec todowrite-postgres psql -U mcp_user -d todowrite -c "SELECT current_database();"

# Check container naming
docker ps | grep -i prod
```

#### Safe Development Practices
```bash
# Use development database for testing
export DATABASE_URL="postgresql://user:pass@localhost:5433/todowrite_dev"

# Create test tables with clear naming
CREATE TABLE test_user_migration_2024_01_15 (LIKE users INCLUDING ALL);

# Use transactions for safety
BEGIN;
-- Your operation here
ROLLBACK;  -- or COMMIT if verified correct
```

### Migration Safety

#### Migration Script Requirements
```python
# ✅ CORRECT - Safe migration approach
def upgrade_user_table():
    """Add email verification field to users table."""
    # Check if column already exists
    if not column_exists('users', 'email_verified'):
        # Add column with default value
        op.add_column('users', sa.Column('email_verified', sa.Boolean(), default=False))

        # Update existing records
        op.execute("UPDATE users SET email_verified = true WHERE email IS NOT NULL")

def downgrade_user_table():
    """Remove email verification field from users table."""
    # Verify it's safe to remove
    if column_exists('users', 'email_verified'):
        op.drop_column('users', 'email_verified')
```

#### Migration Testing Protocol
```bash
# Test migration on copy of production data
pg_dump todowrite | psql todowrite_migration_test

# Run migration on test database
PYTHONPATH="src" python -m alembic upgrade head

# Verify data integrity
python scripts/verify_data_integrity.py

# Performance test migration
python scripts/benchmark_migration.py
```

### Data Loss Prevention

#### Backup Requirements
```bash
# Before any destructive operation
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="todowrite_backup_${TIMESTAMP}.sql"

# Create database backup
pg_dump todowrite > "$BACKUP_FILE"

# Verify backup was created
ls -lh "$BACKUP_FILE"

# Test backup restore (in development)
pg_restore -d todowrite_test "$BACKUP_FILE"
```

#### Recovery Procedures
```bash
# If data loss occurs
1. STOP all application services
2. IDENTIFY the scope of data loss
3. RESTORE from most recent backup
4. VERIFY data integrity
5. ANALYZE root cause
6. IMPLEMENT prevention measures
```

### Code Safety Checks

#### Pre-Deployment Safety Checklist
```python
def safety_check_before_deployment():
    """Comprehensive safety check before deployment."""
    checks = [
        verify_not_production_database(),
        verify_backups_exist(),
        verify_migration_scripts_tested(),
        verify_no_drop_statements(),
        verify_no_truncate_statements(),
        verify_conditional_deletes(),
        verify_foreign_key_constraints(),
    ]

    return all(checks)

def verify_no_drop_statements():
    """Check for DROP statements in code."""
    dangerous_files = []
    for file in get_all_code_files():
        if 'DROP TABLE' in file_content or 'DROP DATABASE' in file_content:
            dangerous_files.append(file)
    return len(dangerous_files) == 0
```

### Incident Response

#### Data Loss Incident Protocol
1. **IMMEDIATE ACTION**: Stop all write operations
2. **ASSESSMENT**: Determine scope of data loss
3. **NOTIFICATION**: Alert stakeholders immediately
4. **RECOVERY**: Begin restoration from backups
5. **INVESTIGATION**: Determine root cause
6. **PREVENTION**: Implement measures to prevent recurrence

#### Incident Documentation
```bash
# Create incident report
cat > incident_$(date +%Y%m%d_%H%M%S).md << EOF
# Data Loss Incident Report

## Time of Incident
$(date)

## Severity
[Critical/High/Medium/Low]

## Impact Description
[Brief description of what happened]

## Root Cause Analysis
[What caused the incident]

## Recovery Actions
[Steps taken to recover]

## Prevention Measures
[How to prevent this in the future]

## Lessons Learned
[Key takeaways from the incident]
EOF
```

### Compliance Requirements

#### Before Submitting Work
1. ✅ Verified not running against production data
2. ✅ No DROP TABLE statements in code
3. ✅ No TRUNCATE statements in code
4. ✅ Conditional DELETE statements with proper WHERE clauses
5. ✅ All schema changes via migration scripts
6. ✅ Migration scripts tested on development data
7. ✅ Backup procedures documented and tested
8. ✅ Data integrity checks implemented
9. ✅ Rollback procedures documented
10. ✅ Incident response procedures understood

### Safe Development Workflow

```bash
# 1. Create development environment
cp .env.example .env.dev
# Edit .env.dev to point to development database

# 2. Test operations on development data
export DATABASE_URL="postgresql://user:pass@localhost:5433/todowrite_dev"

# 3. Verify operations are safe
python scripts/safety_check.py

# 4. Create backup before changes
./scripts/create_backup.sh

# 5. Perform operations
python migration_script.py

# 6. Verify results
python scripts/verify_data_integrity.py

# 7. Document changes
echo "$(date): Performed safe database operation" >> operations.log
```
