# Architecture Documentation

This document describes the architecture and design of the AI Leads Analyzer system.

## System Overview

The AI Leads Analyzer is a FastAPI-based backend service that processes, stores, and analyzes lead information using AI/ML capabilities. The system ingests lead data from multiple sources, enriches it with AI analysis, and provides APIs for data retrieval.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        API Layer                                 │
│  ┌──────────────────┬──────────────────┬──────────────────┐    │
│  │ Ping Endpoint    │ Ingress Endpoint │ Egress Endpoint  │    │
│  └──────────────────┴──────────────────┴──────────────────┘    │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    Application Layer                             │
│  ┌──────────────────┬──────────────────┬──────────────────┐    │
│  │ Dependencies     │ CRUD Operations  │ LLM Service      │    │
│  │ Database Setup   │ Lead Management  │ AI Classification│    │
│  └──────────────────┴──────────────────┴──────────────────┘    │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                   Data Layer                                     │
│  ┌──────────────────┬──────────────────┐                        │
│  │ SQLAlchemy ORM   │ Models           │                        │
│  │ Alembic Migrations│ AllLeads Table  │                        │
│  └──────────────────┴──────────────────┘                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                PostgreSQL Database                               │
│              Persistent Data Storage                             │
└─────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. API Layer (`app/api/`)

The API layer handles HTTP requests and responses using FastAPI.

**Components:**

- **Router**: Organizes endpoints into logical groups
  - `v1/endpoints/ping.py`: Health check endpoints
  - `v1/endpoints/ingress.py`: Lead ingestion endpoints
  - `v1/endpoints/egress.py`: Lead retrieval endpoints

- **Dependencies** (`api/deps.py`): Manages request-level dependencies
  - Database session injection
  - Authentication (future)

- **API Router** (`v1/api.py`): Combines all endpoint routers

### 2. Application Layer

#### Core Module (`app/core/`)

Configuration and security utilities:

- **config.py**: Application configuration and environment variables
- **security.py**: Security utilities and authentication helpers

#### Schemas (`app/schemas/`)

Pydantic models for request/response validation:

- **ingress_schema.py**: Lead input/creation schemas
- **egress_schema.py**: Lead output/response schemas
- **llm_schema.py**: LLM-related schemas
- **ping.py**: Health check schemas

#### CRUD Operations (`app/crud/`)

Database operations for entities:

- **crud_lead.py**: Lead creation, retrieval, update operations
- **constants.py**: Application constants

#### LLM Service (`app/llm/`)

AI/ML integration for lead analysis:

- **llm_client.py**: OpenAI API client wrapper
- **llm_service.py**: Business logic for lead classification and analysis

### 3. Data Layer (`app/db/`)

Database abstraction and models:

- **db.py**: Database connection and session management
- **models/leads_model.py**: SQLAlchemy model for leads table

### 4. Main Application (`app/main.py`)

FastAPI application initialization and startup:

- Creates FastAPI instance
- Registers API routers
- Configures middleware (future)
- Starts Uvicorn server

## Data Flow

### Lead Creation Flow

```
Client Request
    │
    ▼
POST /api/v1/leads/
    │
    ▼
Validate Payload (Pydantic)
    │
    ▼
Create Lead (CRUD)
    │
    ▼
Save to Database
    │
    ▼
Classify with LLM (Optional)
    │
    ▼
Return Response
    │
    ▼
Client Response
```

### Lead Retrieval Flow

```
Client Request
    │
    ▼
GET /api/v1/leads/[?query_params]
    │
    ▼
Query Database (CRUD)
    │
    ▼
Validate Response (Pydantic)
    │
    ▼
Return Response
    │
    ▼
Client Response
```

## Database Schema

### AllLeads Table

```sql
CREATE TABLE all_leads (
    id INTEGER PRIMARY KEY,
    record_inserted_at TIMESTAMP DEFAULT NOW(),
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
```

## Request/Response Validation

Pydantic models ensure data validation at the application boundary:

1. **Ingress Validation**: LeadPayload and sub-models validate incoming lead data
2. **Egress Validation**: Response models ensure outgoing data meets specifications
3. **Type Safety**: All fields have explicit types and constraints
4. **Error Handling**: Validation errors return 422 status with field-level details

## Configuration Management

Environment variables are loaded from `.env` file:

- **Database URL**: Connection string for PostgreSQL
- **OpenAI API Key**: Credentials for LLM service
- **Environment**: Development vs Production
- **Debug**: Debug mode toggle
- **Log Level**: Logging configuration

See [SETUP.md](./SETUP.md) for environment configuration details.

## LLM Integration

The system integrates with OpenAI's GPT-4 model for lead classification:

- **Client**: `app/llm/llm_client.py` - Handles API communication
- **Service**: `app/llm/llm_service.py` - Implements classification logic
- **Features**:
  - Lead classification (AI-related vs non-AI)
  - AI reason extraction
  - Lead scoring and analysis

## Error Handling

Error handling follows these principles:

1. **Validation Errors**: Return 422 with field details
2. **Resource Not Found**: Return 404
3. **Server Errors**: Return 500 with appropriate logging
4. **Database Errors**: Catch and transform to HTTP responses

## Security Considerations

### Current Implementation

- No authentication/authorization (planned for future)
- Environment variables for secrets management
- Input validation via Pydantic

### Recommendations for Production

1. Implement JWT authentication
2. Add rate limiting
3. Enable CORS with specific origins
4. Add request logging and monitoring
5. Use HTTPS only
6. Implement API key management for LLM service

## Scalability

### Current Design

- Single process FastAPI application
- Single database connection pool
- Synchronous request handling

### Scaling Strategies

1. **Horizontal Scaling**: Run multiple instances with load balancer
2. **Async Processing**: Use Celery for long-running LLM operations
3. **Caching**: Implement Redis for frequently accessed leads
4. **Database Optimization**: Add indexes on frequently queried columns
5. **Microservices**: Separate LLM service into dedicated microservice

## Development Workflow

1. Create feature branch from `main`
2. Make changes following code style guidelines
3. Run tests and linters
4. Submit pull request for review
5. Merge after approval
6. Deploy to staging/production

See [DEVELOPMENT.md](./DEVELOPMENT.md) for detailed development guidelines.

## Monitoring and Logging

### Current Implementation

- Uvicorn logging (configurable)
- Application logs via Python logging

### Recommendations

1. Centralized logging (ELK stack, CloudWatch)
2. Application metrics (Prometheus)
3. Distributed tracing (Jaeger)
4. Error tracking (Sentry)
5. Health check monitoring

## Future Enhancements

- [ ] Async request processing
- [ ] WebSocket support for real-time updates
- [ ] Advanced lead segmentation
- [ ] ML model fine-tuning
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
