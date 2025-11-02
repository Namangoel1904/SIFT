# SIFT API Contract

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Currently, the API does not require authentication. In production, implement API keys or OAuth2.

## Endpoints

### 1. Analyze Text

**Endpoint**: `POST /analyze/text`

**Description**: Analyzes text content and fact-checks claims found within it.

**Request Body**:
```json
{
  "text": "string (required, min 10 characters)",
  "url": "string (optional)"
}
```

**Request Example**:
```json
{
  "text": "The COVID-19 vaccine causes infertility in 99% of recipients. Studies from 2021 show this conclusively.",
  "url": "https://example.com/article"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "claims": [
      {
        "claim": "The COVID-19 vaccine causes infertility in 99% of recipients",
        "type": "statistical"
      }
    ],
    "results": [
      {
        "claim": "The COVID-19 vaccine causes infertility in 99% of recipients",
        "claim_type": "statistical",
        "claim_confidence": 0.8,
        "verdict": "false",
        "confidence": 0.95,
        "explanation": "This claim is false. Multiple studies have shown no link between COVID-19 vaccines and infertility.",
        "evidence": "Studies from CDC, WHO, and peer-reviewed journals confirm no increased infertility risk.",
        "sources": [
          {
            "title": "Fact Check: COVID-19 vaccines and fertility",
            "url": "https://factcheck.org/article/example",
            "snippet": "Multiple studies have debunked claims about vaccine-related infertility..."
          }
        ]
      }
    ],
    "summary": {
      "total_claims": 1,
      "verified_claims": 0,
      "false_claims": 1,
      "partially_true_claims": 0,
      "unverified_claims": 0
    }
  }
}
```

**Error Response** (400/500):
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

### 2. Analyze URL

**Endpoint**: `POST /analyze/url`

**Description**: Fetches content from a URL and analyzes it for fact-checking.

**Request Body**:
```json
{
  "url": "string (required, valid URL)"
}
```

**Request Example**:
```json
{
  "url": "https://example.com/news-article"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "url": "https://example.com/news-article",
    "url_title": "News Article Title",
    "url_description": "Article description",
    "claims": [...],
    "results": [...],
    "summary": {...}
  }
}
```

**Error Response** (400):
```json
{
  "detail": "Could not fetch URL content"
}
```

---

### 3. Health Check

**Endpoint**: `GET /health`

**Description**: Returns API health status.

**Response** (200 OK):
```json
{
  "status": "healthy",
  "service": "SIFT API"
}
```

---

## Data Models

### Verdict Types

- `"true"`: Claim is verified as true
- `"false"`: Claim is verified as false
- `"partially_true"`: Claim is partially true/misleading
- `"unverified"`: Cannot verify with available sources

### Claim Types

- `"statistical"`: Claims involving numbers, percentages, statistics
- `"historical"`: Claims about past events
- `"scientific"`: Scientific claims, research findings
- `"event"`: Claims about specific events
- `"general"`: General factual claims

### Source Object

```typescript
{
  title: string;
  url: string;
  snippet?: string;
  source?: string; // "google", "factcheck.org", etc.
}
```

### Result Object

```typescript
{
  claim: string;
  claim_type: string;
  claim_confidence: number; // 0-1
  verdict: "true" | "false" | "partially_true" | "unverified";
  confidence: number; // 0-1
  explanation: string;
  evidence: string;
  sources: Source[];
}
```

---

## Rate Limiting

Currently not implemented. Recommended limits:
- 10 requests per minute per IP
- 100 requests per hour per IP

---

## Error Codes

- `400`: Bad Request - Invalid input
- `500`: Internal Server Error - Server-side error
- `503`: Service Unavailable - External service failure

---

## Example Usage

### cURL

```bash
# Analyze text
curl -X POST "http://localhost:8000/api/v1/analyze/text" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The Earth is flat according to ancient texts.",
    "url": "https://example.com"
  }'

# Analyze URL
curl -X POST "http://localhost:8000/api/v1/analyze/url" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/article"
  }'
```

### JavaScript (Extension)

```javascript
const response = await fetch('http://localhost:8000/api/v1/analyze/text', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: selectedText,
    url: window.location.href
  })
});

const data = await response.json();
```

### Python

```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/api/v1/analyze/text",
        json={
            "text": "Claim to fact-check...",
            "url": "https://example.com"
        }
    )
    data = response.json()
```

