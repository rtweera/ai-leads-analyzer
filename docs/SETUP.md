# Setup Guide

This guide provides step-by-step instructions to set up the AI Leads Analyzer backend application.

## Prerequisites

- Python 3.12 or higher
- PostgreSQL database (for production use)
- pip or Poetry package manager
- Git

## Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/rtweera/ai-leads-analyzer.git
cd ai-leads-analyzer
```

### 2. Create Virtual Environment

Using Poetry (recommended):

```bash
poetry install
```

Or using venv:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/ai_leads_db

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# FastAPI Configuration
APP_ENV=development
DEBUG=true

# Security
SECRET_KEY=your_secret_key_here

# Additional Configuration
LOG_LEVEL=info
```

### 4. Database Setup

Initialize the database using Alembic migrations:

```bash
alembic upgrade head
```

To create a new migration after model changes:

```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### 5. Run the Application

Using Poetry:

```bash
poetry run python app/main.py
```

Or with Python directly:

```bash
python app/main.py
```

The application will start on `http://localhost:8000`

### 6. Access API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Docker Setup (Optional)

To run the application in a Docker container:

```bash
docker build -t ai-leads-analyzer .
docker run -p 8000:8000 --env-file .env ai-leads-analyzer
```

## Database Configuration

### PostgreSQL Setup

```bash
# Create database
createdb ai_leads_db

# Create database user (optional)
createuser -P ai_leads_user
```

### Connection String Format

```
postgresql://[user[:password]@][host][:port][/database][?param=value]
```

Example:
```
postgresql://ai_leads_user:password@localhost:5432/ai_leads_db
```

## Dependencies

Key dependencies are defined in `pyproject.toml`:

- **FastAPI**: Web framework
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation
- **Alembic**: Database migrations
- **Psycopg2**: PostgreSQL adapter
- **NumPy**: Numerical computing
- **python-dotenv**: Environment variable management

## Troubleshooting

### Import Errors

If you encounter import errors, ensure the Python path includes the project root:

```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/ai-leads-analyzer"
```

### Database Connection Issues

Check that PostgreSQL is running and the connection string in `.env` is correct:

```bash
psql -U user -d ai_leads_db -h localhost
```

### Port Already in Use

If port 8000 is in use, specify a different port:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001
```

## Next Steps

- Read [DEVELOPMENT.md](./DEVELOPMENT.md) for development guidelines
- Check [API.md](./API.md) for API endpoint documentation
- Review [ARCHITECTURE.md](./ARCHITECTURE.md) for system design
- Explore [DATABASE.md](./DATABASE.md) for database schema
