# SIFT Backend - Render Deployment Guide

## Prerequisites

1. Render account
2. All required API keys and credentials

## Environment Variables

Set these in Render dashboard under your service's "Environment" section:

### Required API Keys

```bash
GOOGLE_API_KEY=your_google_gemini_api_key
GOOGLE_SEARCH_API_KEY=your_google_search_api_key
GOOGLE_SEARCH_CX=your_custom_search_engine_id
FACT_CHECK_API_KEY=your_fact_check_api_key
```

### Google Cloud Translation Credentials

**For Render deployment**, use `GOOGLE_CREDENTIALS_JSON` instead of a file path:

1. Get your service account JSON file from Google Cloud Console
2. Copy the entire JSON content
3. In Render, add environment variable:
   - Key: `GOOGLE_CREDENTIALS_JSON`
   - Value: Paste the entire JSON string (all on one line, or use Render's multiline support)

Example:
```json
{"type":"service_account","project_id":"...","private_key_id":"...","private_key":"...","client_email":"...","client_id":"...","auth_uri":"...","token_uri":"...","auth_provider_x509_cert_url":"...","client_x509_cert_url":"..."}
```

### Optional Configuration

```bash
SIFT_GEMINI_MODEL=gemini-2.0-flash
GEMINI_TEMPERATURE=0.1
CACHE_TTL=3600
CORS_ORIGINS=https://your-netlify-app.netlify.app,https://another-domain.com
```

### Server Configuration

Render will automatically set `PORT` environment variable. The start command uses `$PORT`.

## Deployment Steps

1. **Connect Repository**: Connect your GitHub/GitLab repository to Render
2. **Create New Web Service**: 
   - Select your repository
   - Root Directory: `backend` (if repo root is not backend folder)
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Or use: `bash start.sh` (if you prefer the shell script)
3. **Set Environment Variables**: Add all required environment variables in Render dashboard (see below)
4. **Deploy**: Render will automatically deploy on every push to main branch

### Environment Variables Setup in Render

Go to your service → Environment → Add Environment Variable:

**Required:**
- `GOOGLE_API_KEY` = your Google Gemini API key
- `GOOGLE_SEARCH_API_KEY` = your Google Custom Search API key  
- `GOOGLE_SEARCH_CX` = your Custom Search Engine ID
- `FACT_CHECK_API_KEY` = your Fact Check Tools API key
- `GOOGLE_CREDENTIALS_JSON` = full JSON string from service account file

**Optional:**
- `CORS_ORIGINS` = `https://your-app.netlify.app` (comma-separated)
- `SIFT_GEMINI_MODEL` = `gemini-2.0-flash`
- `GEMINI_TEMPERATURE` = `0.1`
- `CACHE_TTL` = `3600`

**Note:** For `GOOGLE_CREDENTIALS_JSON`, copy the entire contents of your service account JSON file and paste it as the value. Render supports multiline strings, but you can also put it all on one line.

## Testing

After deployment, test your endpoints:

### Health Check
```bash
curl https://your-render-app.onrender.com/
```

### Test Text Analysis
```bash
curl -X POST https://your-render-app.onrender.com/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "The Earth is flat."}'
```

### Test URL Analysis
```bash
curl -X POST https://your-render-app.onrender.com/api/v1/analyze/url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/article"}'
```

## CORS Configuration

The backend is configured to accept requests from:
- Chrome extensions
- Localhost (development)
- Netlify domains (*.netlify.app, *.netlify.com)
- Additional domains via `CORS_ORIGINS` environment variable

## Troubleshooting

### Translation Service Not Working

1. Verify `GOOGLE_CREDENTIALS_JSON` is set correctly
2. Check that the JSON is valid (no newlines, properly escaped)
3. Check Render logs for authentication errors

### CORS Errors

1. Ensure your frontend domain is in `CORS_ORIGINS`
2. Check that `allow_credentials=True` is set (already configured)
3. Verify frontend is sending correct headers

### Port Issues

Render automatically sets `PORT`. Make sure start command uses `$PORT`:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

