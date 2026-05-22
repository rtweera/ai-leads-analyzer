# AI Leads Analyzer

A FastAPI-based backend service for analyzing and managing leads using artificial intelligence.

## Overview

The AI Leads Analyzer is a modern web application backend that ingests lead information from multiple sources, stores it in a PostgreSQL database, and uses AI (OpenAI GPT-4) to classify and analyze leads. The service provides RESTful APIs for lead management and retrieval.

### Key Features

- 📧 **Lead Ingestion**: Accept lead data from email and other sources
- 🤖 **AI Classification**: Automatically classify leads as AI-related or non-AI using OpenAI GPT-4
- 💾 **Persistent Storage**: Store leads in PostgreSQL with rich queryable metadata
- 🔍 **Lead Retrieval**: Query and retrieve leads with pagination and filtering
- 📊 **Data Analysis**: Analyze lead patterns and trends
- 🚀 **RESTful API**: Clean, well-documented REST API endpoints
- 📚 **Interactive Documentation**: Built-in Swagger UI and ReDoc for API exploration

## Technology Stack

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for Python
- **Database**: [PostgreSQL](https://www.postgresql.org/) - Reliable relational database
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM
- **Data Validation**: [Pydantic](https://docs.pydantic.dev/) - Data validation using Python type annotations
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/) - Database schema migrations
- **AI Service**: [OpenAI API](https://platform.openai.com/) - GPT-4 for lead classification
- **Server**: [Uvicorn](https://www.uvicorn.org/) - ASGI web server

## Quick Start

### Prerequisites

- Python 3.12 or higher
- PostgreSQL 12 or higher
- OpenAI API key

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/rtweera/ai-leads-analyzer.git
cd ai-leads-analyzer
```

2. **Install dependencies**

```bash
poetry install
```

3. **Configure environment**

```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Initialize database**

```bash
alembic upgrade head
```

5. **Run the application**

```bash
poetry run python app/main.py
```

The API will be available at `http://localhost:8000`

### Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[SETUP.md](./docs/SETUP.md)** - Installation and environment setup
- **[API.md](./docs/API.md)** - Complete API endpoint documentation
- **[ARCHITECTURE.md](./docs/ARCHITECTURE.md)** - System design and architecture
- **[DEVELOPMENT.md](./docs/DEVELOPMENT.md)** - Development guidelines and workflow
- **[DATABASE.md](./docs/DATABASE.md)** - Database schema and queries

## Project Structure

```
ai-leads-analyzer/
├── app/                          # Application code
│   ├── api/                      # API endpoints
│   │   ├── v1/
│   │   │   ├── endpoints/        # Endpoint implementations
│   │   │   └── api.py            # API router
│   │   └── deps.py               # Dependencies
│   ├── core/                     # Core functionality
│   │   ├── config.py             # Configuration
│   │   └── security.py           # Security utilities
│   ├── schemas/                  # Pydantic models
│   ├── crud/                     # Database operations
│   ├── db/                       # Database models
│   ├── llm/                      # LLM integration
│   └── main.py                   # Application entry
├── docs/                         # Documentation
├── alembic/                      # Database migrations
├── pyproject.toml               # Project configuration
└── README.md                    # This file
```

## API Endpoints

### Health Check

```
GET /api/v1/ping
```

### Lead Management

```
POST   /api/v1/leads/          # Create new lead
GET    /api/v1/leads/          # Retrieve all leads
GET    /api/v1/leads/{id}      # Retrieve specific lead
```

See [API.md](./docs/API.md) for complete endpoint documentation.

## Usage Examples

### Create a Lead

```bash
curl -X POST "http://localhost:8000/api/v1/leads/" \
  -H "Content-Type: application/json" \
  -d '{
    "emailInfo": {
      "subject": "NEW LEAD",
      "from": "sender@example.com",
      "to": ["recipient@example.com"],
      "cc": []
    },
    "leadInfo": {
      "firstName": "John",
      "lastName": "Doe",
      "email": "john@example.com",
      "phone": "+1234567890",
      "jobTitle": "Software Engineer",
      "company": "Tech Corp",
      "country": "USA",
      "state": "CA",
      "areaOfInterest": "API Management",
      "contactReason": "Product Inquiry",
      "industry": "Technology",
      "canHelpComment": "Interested in solutions"
    }
  }'
```

### Retrieve All Leads

```bash
curl -X GET "http://localhost:8000/api/v1/leads/?skip=0&limit=10"
```

### Retrieve Specific Lead

```bash
curl -X GET "http://localhost:8000/api/v1/leads/1"
```

## Development

### Setup Development Environment

```bash
poetry install
cp .env.example .env.development
# Edit configuration
```

### Run Tests

```bash
pytest
```

### Run Linters

```bash
pylint app/
black app/ --check
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

See [DEVELOPMENT.md](./docs/DEVELOPMENT.md) for detailed development guidelines.

## Configuration

Configure the application using environment variables in `.env`:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ai_leads_db

# OpenAI
OPENAI_API_KEY=sk-...

# Application
APP_ENV=development
DEBUG=true
LOG_LEVEL=info

# Security
SECRET_KEY=your-secret-key
```

See [SETUP.md](./docs/SETUP.md) for complete configuration options.

## Architecture

The application follows a layered architecture:

1. **API Layer**: HTTP endpoint handlers
2. **Application Layer**: Business logic and services
3. **Data Layer**: Database models and operations
4. **External Services**: OpenAI, PostgreSQL

See [ARCHITECTURE.md](./docs/ARCHITECTURE.md) for detailed architecture documentation.

## Database

The application uses PostgreSQL with the following main table:

- **all_leads**: Stores lead information and AI analysis results

See [DATABASE.md](./docs/DATABASE.md) for schema details and common queries.

## Features

### Lead Ingestion
- Accept lead data from email and webhooks
- Validate and normalize input data
- Store structured lead information

### AI Analysis
- Classify leads using OpenAI GPT-4
- Extract AI-related insights
- Determine lead relevance

### Lead Management
- Store leads in PostgreSQL
- Query leads with pagination
- Filter by various criteria
- Track lead metadata

### API
- RESTful endpoints
- JSON request/response format
- Comprehensive error handling
- Interactive API documentation

## Performance

- Single-instance deployment: ~100 requests/second
- Database connection pooling: 10-20 connections
- Response times: <100ms for typical queries
- Support for pagination and filtering

### Scaling Recommendations

- Use load balancer for multiple instances
- Implement Redis caching for frequently accessed data
- Optimize database indexes
- Use async processing for LLM calls
- Consider microservices architecture

See [ARCHITECTURE.md](./docs/ARCHITECTURE.md) for scaling strategies.

## Security

### Current Implementation

- Input validation with Pydantic
- Environment-based configuration
- No authentication (planned for future)

### Recommendations for Production

- Implement JWT authentication
- Enable HTTPS/TLS
- Add rate limiting
- Implement CORS
- Add API key management
- Enable database encryption
- Set up proper logging and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/name`
3. Make changes and commit: `git commit -am "Add feature"`
4. Push to branch: `git push origin feature/name`
5. Submit a pull request

See [DEVELOPMENT.md](./docs/DEVELOPMENT.md) for contribution guidelines.

## License

This project is licensed under the Apache License 2.0. See LICENSE file for details.

## Contact

**Author**: Ravindu Weerasinghe  
**Email**: ravindutharuka2001@gmail.com

## Changelog

### Version 0.1.0

Initial release with:
- Lead ingestion via API
- Lead storage in PostgreSQL
- OpenAI GPT-4 integration
- Lead retrieval endpoints
- API documentation

## Roadmap

### Upcoming Features

- [ ] User authentication and authorization
- [ ] Advanced lead segmentation
- [ ] ML model fine-tuning
- [ ] WebSocket support for real-time updates
- [ ] Analytics dashboard
- [ ] Multi-language support
- [ ] Lead export (CSV, PDF)
- [ ] Webhook integrations
- [ ] Rate limiting and throttling
- [ ] Advanced search capabilities

## Support

For issues, questions, or suggestions:

1. Check the [documentation](./docs/)
2. Review existing GitHub issues
3. Create a new issue with detailed information
4. Contact the development team

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Uvicorn Documentation](https://www.uvicorn.org/)