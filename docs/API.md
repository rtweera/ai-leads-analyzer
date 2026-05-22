# API Documentation

This document describes the REST API endpoints for the AI Leads Analyzer service.

## Base URL

```
http://localhost:8000/api/v1
```

## Overview

The API provides endpoints to manage leads, retrieve lead information, and analyze lead data using AI.

## Authentication

Currently, the API is open. Future versions may require authentication.

## Response Format

All responses are in JSON format. Successful responses include a `200`, `201`, or `204` status code. Error responses include a `4xx` or `5xx` status code with an error message.

### Success Response Example

```json
{
  "message": "Success message",
  "data": {}
}
```

### Error Response Example

```json
{
  "detail": "Error message"
}
```

## Endpoints

### Health Check

#### GET /ping

Check if the API is running.

**Response:**

```json
{
  "ping": "pong"
}
```

**Status Code:** `200 OK`

---

### Leads Management

#### POST /leads/

Create a new lead record.

**Request Body:**

```json
{
  "emailInfo": {
    "subject": "NEW LEAD from: Bonjour | Alfonso | API Management Contact Us",
    "from": "example@example.com",
    "to": ["johndoe@wso2.com"],
    "cc": ["johndoe@wso2.com", "mail2@example.com"]
  },
  "leadInfo": {
    "firstName": "John",
    "lastName": "Doe",
    "email": "John@example.com",
    "phone": "+1234567890",
    "jobTitle": "Developer / Engineer",
    "company": "WSO2",
    "country": "Sri Lanka",
    "state": "Western",
    "areaOfInterest": "API",
    "contactReason": "Other",
    "industry": "IT",
    "canHelpComment": "Test comment"
  }
}
```

**Request Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| emailInfo | object | Yes | Email metadata |
| emailInfo.subject | string | Yes | Email subject |
| emailInfo.from | string | Yes | Sender email address |
| emailInfo.to | array | Yes | Recipient email addresses |
| emailInfo.cc | array | No | CC email addresses |
| leadInfo | object | Yes | Lead information |
| leadInfo.firstName | string | Yes | Lead's first name |
| leadInfo.lastName | string | Yes | Lead's last name |
| leadInfo.email | string | Yes | Lead's email address |
| leadInfo.phone | string | No | Lead's phone number |
| leadInfo.jobTitle | string | Yes | Lead's job title |
| leadInfo.company | string | Yes | Lead's company |
| leadInfo.country | string | Yes | Lead's country |
| leadInfo.state | string | No | Lead's state/province |
| leadInfo.areaOfInterest | string | Yes | Area of interest (e.g., API) |
| leadInfo.contactReason | string | Yes | Reason for contact |
| leadInfo.industry | string | Yes | Industry type |
| leadInfo.canHelpComment | string | Yes | Additional comments |

**Response:**

```json
{
  "message": "Lead created successfully",
  "lead": {
    "emailInfo": {...},
    "leadInfo": {...}
  }
}
```

**Status Code:** `201 Created`

**Error Responses:**

- `400 Bad Request`: Invalid request format
- `422 Unprocessable Entity`: Validation error on request fields
- `500 Internal Server Error`: Server error during creation

---

#### GET /leads/

Retrieve all leads.

**Query Parameters:** (Optional)

| Parameter | Type | Description |
|-----------|------|-------------|
| skip | integer | Number of records to skip (default: 0) |
| limit | integer | Number of records to return (default: 10) |

**Response:**

```json
[
  {
    "id": 1,
    "lead_first_name": "John",
    "lead_last_name": "Doe",
    "lead_email": "john@example.com",
    "lead_company": "WSO2",
    "is_about_ai": true,
    "record_inserted_at": "2024-01-15T10:30:00Z"
  }
]
```

**Status Code:** `200 OK`

---

#### GET /leads/{lead_id}

Retrieve a specific lead by ID.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| lead_id | integer | The ID of the lead |

**Response:**

```json
{
  "id": 1,
  "lead_first_name": "John",
  "lead_last_name": "Doe",
  "lead_email": "john@example.com",
  "lead_company": "WSO2",
  "lead_country": "Sri Lanka",
  "lead_industry": "IT",
  "is_about_ai": true,
  "ai_reason": "Mentioned API and AI technologies",
  "record_inserted_at": "2024-01-15T10:30:00Z"
}
```

**Status Code:** `200 OK`

**Error Responses:**

- `404 Not Found`: Lead not found

---

## Rate Limiting

Currently, there are no rate limits. Future versions may implement rate limiting.

## Pagination

Paginated endpoints support the following query parameters:

- `skip`: Number of records to skip
- `limit`: Number of records to return (max: 100)

## Error Codes

| Code | Message | Description |
|------|---------|-------------|
| 400 | Bad Request | The request is invalid or malformed |
| 404 | Not Found | The requested resource was not found |
| 422 | Unprocessable Entity | Validation failed on input data |
| 500 | Internal Server Error | Server encountered an error |

## Usage Examples

### Create a Lead using cURL

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
      "canHelpComment": "Interested in API solutions"
    }
  }'
```

### Retrieve All Leads using cURL

```bash
curl -X GET "http://localhost:8000/api/v1/leads/?skip=0&limit=10" \
  -H "Accept: application/json"
```

### Using Python Requests

```python
import requests

# Create a lead
response = requests.post(
    "http://localhost:8000/api/v1/leads/",
    json={
        "emailInfo": {...},
        "leadInfo": {...}
    }
)
print(response.json())

# Retrieve all leads
response = requests.get("http://localhost:8000/api/v1/leads/")
print(response.json())
```

## Interactive API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These tools provide interactive exploration of all available endpoints with example payloads.
