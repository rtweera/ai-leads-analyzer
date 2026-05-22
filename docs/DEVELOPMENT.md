# Development Guide

This guide provides guidelines and best practices for developing the AI Leads Analyzer application.

## Project Structure

```
ai-leads-analyzer/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── ping.py
│   │   │   │   ├── ingress.py
│   │   │   │   └── egress.py
│   │   │   └── api.py
│   │   ├── deps.py
│   │   └── __init__.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── ingress_schema.py
│   │   ├── egress_schema.py
│   │   ├── llm_schema.py
│   │   ├── ping.py
│   │   └── __init__.py
│   ├── crud/
│   │   ├── crud_lead.py
│   │   ├── constants.py
│   │   └── __init__.py
│   ├── db/
│   │   ├── db.py
│   │   ├── models/
│   │   │   ├── leads_model.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── llm/
│   │   ├── llm_client.py
│   │   ├── llm_service.py
│   │   └── __init__.py
│   ├── main.py
│   └── __init__.py
├── docs/
├── pyproject.toml
└── poetry.lock
```

## Setup Development Environment

### 1. Prerequisites

- Python 3.12+
- PostgreSQL 12+
- Git

### 2. Clone and Install

```bash
git clone https://github.com/rtweera/ai-leads-analyzer.git
cd ai-leads-analyzer

# Install dependencies
poetry install
```

### 3. Configure Environment

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env` with local database and API credentials.

### 4. Initialize Database

```bash
# Create database
createdb ai_leads_db_dev

# Run migrations
alembic upgrade head
```

## Code Style and Standards

### Python Style Guide

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) conventions:

- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use meaningful variable and function names
- Add docstrings to functions and classes

### Naming Conventions

```python
# Classes: PascalCase
class LeadProcessor:
    pass

# Functions/Methods: snake_case
def create_lead():
    pass

# Constants: UPPER_SNAKE_CASE
DATABASE_URL = "postgresql://..."

# Private methods/attributes: _leading_underscore
def _internal_helper():
    pass
```

### Docstring Format

Use Google-style docstrings:

```python
def create_lead(db: Session, lead_payload: LeadPayload) -> Lead:
    """
    Create a new lead in the database.
    
    Args:
        db: SQLAlchemy database session
        lead_payload: Lead data payload
        
    Returns:
        Lead: Created lead object
        
    Raises:
        ValueError: If lead data is invalid
        DatabaseError: If database operation fails
    """
    pass
```

## Development Workflow

### 1. Feature Branch

Create a feature branch for each task:

```bash
git checkout -b feature/lead-classification
git checkout -b fix/database-connection-issue
git checkout -b docs/api-documentation
```

Branch naming conventions:
- `feature/`: New features
- `fix/`: Bug fixes
- `docs/`: Documentation
- `test/`: Test additions
- `refactor/`: Code refactoring

### 2. Make Changes

```bash
# Edit files
# Run tests
pytest

# Check code style
pylint app/

# Format code
black app/
```

### 3. Commit Changes

Use clear, descriptive commit messages:

```bash
git add .
git commit -m "feat: add lead classification endpoint"
git commit -m "fix: resolve database connection timeout"
git commit -m "docs: add API documentation"
```

Commit message format: `<type>: <description>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Test addition/modification
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `chore`: Build, dependency updates

### 4. Push and Create PR

```bash
git push origin feature/lead-classification
# Create pull request on GitHub
```

PR checklist:
- [ ] Code follows style guide
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Includes description of changes

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_leads.py

# Run with coverage
pytest --cov=app tests/

# Run with verbose output
pytest -v
```

### Writing Tests

Create test files in a `tests/` directory:

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_lead():
    """Test lead creation endpoint."""
    response = client.post(
        "/api/v1/leads/",
        json={
            "emailInfo": {...},
            "leadInfo": {...}
        }
    )
    assert response.status_code == 201
    assert response.json()["message"] == "Lead created successfully"

def test_get_leads():
    """Test retrieve leads endpoint."""
    response = client.get("/api/v1/leads/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

### Test Coverage Goals

- Minimum 80% code coverage
- All public API endpoints tested
- Edge cases and error conditions covered
- Integration tests for database operations

## Logging and Debugging

### Logging

Use Python's logging module:

```python
import logging

logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Debug Mode

Enable debug mode in `.env`:

```env
DEBUG=true
```

Run with verbose logging:

```bash
python app/main.py --log-level debug
```

## Database Migrations

### Creating a Migration

After modifying models, create a migration:

```bash
alembic revision --autogenerate -m "Add new column to leads table"
```

Review the generated migration file in `alembic/versions/`:

```bash
# Check migrations without applying
alembic current

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Migration Best Practices

1. Always review auto-generated migrations
2. Write descriptive migration messages
3. Test migrations in development
4. Never commit `__pycache__` directories or `.pyc` files to version control (they are auto-generated bytecode)
5. Keep migrations reversible

## API Development

### Adding New Endpoints

1. **Create Schema** (`app/schemas/`):

```python
from pydantic import BaseModel

class NewEndpointRequest(BaseModel):
    field1: str
    field2: int
```

2. **Create Endpoint** (`app/api/v1/endpoints/`):

```python
from fastapi import APIRouter, Depends
from app.schemas.new_schema import NewEndpointRequest
from app.api.deps import get_db

router = APIRouter()

@router.post("/", tags=["New Feature"], response_model=dict, status_code=201)
async def create_resource(request: NewEndpointRequest, db: Session = Depends(get_db)):
    """Create a new resource."""
    # Implementation
    return {"message": "Success"}
```

3. **Register Router** (`app/api/v1/api.py`):

```python
from app.api.v1.endpoints import new_endpoints

api_router.include_router(new_endpoints.router, prefix="/new", tags=["New"])
```

## Performance Optimization

### Database Optimization

- Use database indexes on frequently queried columns
- Avoid N+1 queries using SQLAlchemy eager loading
- Use connection pooling
- Monitor slow queries

### Code Optimization

- Cache frequently accessed data
- Use async operations for I/O-bound tasks
- Profile code with `cProfile`
- Minimize external API calls

## Security Considerations

### Input Validation

- Always validate user input using Pydantic
- Sanitize data before storing in database
- Use parameterized queries to prevent SQL injection

### Secrets Management

- Never commit `.env` file
- Use environment variables for secrets
- Rotate API keys regularly
- Use secure connections (HTTPS)

### Error Handling

- Don't expose sensitive information in error messages
- Log errors securely
- Use generic error messages for external APIs

## Common Issues and Solutions

### Issue: Database Connection Timeout

**Solution:** Check PostgreSQL is running and connection string is correct:

```bash
psql -U user -d ai_leads_db -h localhost
```

### Issue: Import Errors

**Solution:** Add project root to Python path:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Issue: Port Already in Use

**Solution:** Use different port:

```bash
python -m uvicorn app.main:app --port 8001
```

### Issue: Module Not Found

**Solution:** Reinstall dependencies:

```bash
poetry install
```

## Code Review Process

1. Create pull request with description
2. Request review from team members
3. Address review comments
4. Ensure CI/CD pipeline passes
5. Merge after approval

## Documentation

- Update README when adding major features
- Keep docstrings synchronized with code
- Add inline comments for complex logic
- Update API documentation in [API.md](./API.md)
- Add architecture changes to [ARCHITECTURE.md](./ARCHITECTURE.md)

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python Logging](https://docs.python.org/3/library/logging.html)
- [Git Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows)

## Getting Help

- Check existing issues on GitHub
- Review project documentation
- Ask in project discussions
- Consult with team members
