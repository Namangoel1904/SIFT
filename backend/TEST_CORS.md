# Test CORS Configuration

## Quick Test Commands

### 1. Test Preflight Request (OPTIONS)

```bash
curl -X OPTIONS https://sift-api.onrender.com/api/v1/analyze \
  -H "Origin: https://siftdetect.netlify.app" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -i
```

**Expected Response:**
- Status: `204 No Content` or `200 OK`
- Headers should include:
  - `Access-Control-Allow-Origin: https://siftdetect.netlify.app`
  - `Access-Control-Allow-Methods: POST, GET, ...`
  - `Access-Control-Allow-Headers: *`

### 2. Check Debug Endpoint (After Deploying Code)

After pushing the code with `/cors-debug` endpoint:

```bash
curl https://sift-api.onrender.com/cors-debug
```

Should show:
```json
{
  "cors_origins": [...],
  "env_cors_origins": "...",
  "allow_all_origins": "..."
}
```

### 3. Test Actual POST Request

```bash
curl -X POST https://sift-api.onrender.com/api/v1/analyze \
  -H "Origin: https://siftdetect.netlify.app" \
  -H "Content-Type: application/json" \
  -d '{"text": "test"}' \
  -i
```

## If CORS Still Fails

The most common issue is that `CORS_ORIGINS` environment variable is:
1. **Not set** - Set it in Render
2. **Set incorrectly** - Should be exactly: `https://siftdetect.netlify.app`
3. **Service not restarted** - Wait 1-2 minutes after setting env var

## Quick Fix Steps

1. **Set ALLOW_ALL_ORIGINS=true** (temporary, for testing)
2. **Wait for service restart**
3. **Test your Netlify site** - should work now
4. **Once confirmed, set CORS_ORIGINS properly:**
   - Remove ALLOW_ALL_ORIGINS
   - Set CORS_ORIGINS=https://siftdetect.netlify.app
5. **Test again** - should still work

