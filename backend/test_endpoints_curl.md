# SIFT API Test Commands

## Quick Smoke Tests

Replace `YOUR_RENDER_URL` with your actual Render service URL (e.g., `https://sift-api.onrender.com`)

### 1. Health Check

```bash
curl https://YOUR_RENDER_URL/
```

**Expected Response:**
```json
{
  "message": "SIFT API - AI Misinformation Prevention & Fact-Checking",
  "version": "1.0.0",
  "docs": "/docs"
}
```

### 2. Text Analysis

```bash
curl -X POST https://YOUR_RENDER_URL/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "The Earth is flat."}'
```

**Expected Response:**
```json
{
  "claims": [...],
  "summary": "...",
  "methodology": "...",
  "limitations": "..."
}
```

### 3. URL Analysis

```bash
curl -X POST https://YOUR_RENDER_URL/api/v1/analyze/url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.bbc.com/news/science-environment"}'
```

### 4. Test CORS (from frontend domain)

```bash
curl -X OPTIONS https://YOUR_RENDER_URL/api/v1/analyze \
  -H "Origin: https://your-app.netlify.app" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v
```

**Expected:** Should include `Access-Control-Allow-Origin` header

### 5. Full Analysis with Verbose Output

```bash
curl -X POST https://YOUR_RENDER_URL/api/v1/analyze \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "text": "Climate change is a hoax perpetrated by scientists."
  }' \
  -w "\n\nHTTP Status: %{http_code}\nTime: %{time_total}s\n" \
  -v
```

## Testing with jq (Pretty Print JSON)

If you have `jq` installed:

```bash
curl -X POST https://YOUR_RENDER_URL/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Test claim here"}' | jq '.'
```

## Error Testing

### Missing Required Field

```bash
curl -X POST https://YOUR_RENDER_URL/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Expected:** 422 Validation Error

### Invalid URL

```bash
curl -X POST https://YOUR_RENDER_URL/api/v1/analyze/url \
  -H "Content-Type: application/json" \
  -d '{"url": "not-a-valid-url"}'
```

**Expected:** 422 Validation Error

## Performance Testing

```bash
time curl -X POST https://YOUR_RENDER_URL/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a test claim for performance testing."}'
```

## Windows PowerShell Alternative

If using Windows PowerShell:

```powershell
Invoke-RestMethod -Uri "https://YOUR_RENDER_URL/api/v1/analyze" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"text": "The Earth is flat."}' | ConvertTo-Json
```

## Browser Testing

Open in browser:
```
https://YOUR_RENDER_URL/docs
```

This will show the interactive API documentation (Swagger UI).

