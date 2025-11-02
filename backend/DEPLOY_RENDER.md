# SIFT Backend - Render Deployment Guide

## Prerequisites

1. Render account (sign up at https://render.com)
2. GitHub/GitLab account (to connect repository)
3. All required API keys and credentials (see below)

## Step-by-Step Deployment

### 1. Prepare Your Credentials

Before deploying, gather all required credentials:

**Google API Keys:**
- Google Gemini API Key (from https://makersuite.google.com/app/apikey)
- Google Custom Search API Key (from Google Cloud Console)
- Google Custom Search Engine ID (CX)
- Google Fact Check Tools API Key
- Google Cloud Translation Service Account JSON

**Getting Translation Credentials:**

**See detailed guide:** `GOOGLE_CREDENTIALS_SETUP.md`

**Quick steps:**
1. Go to Google Cloud Console → IAM & Admin → Service Accounts
2. Create a service account with **Cloud Translation API User** role
3. Download the JSON key file
4. Open the JSON file and **copy the ENTIRE contents** (everything from `{` to `}`)
5. Paste the entire JSON as the value for `GOOGLE_CREDENTIALS_JSON` in Render

**Example JSON structure (you'll have the actual values):**
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "service@project.iam.gserviceaccount.com",
  ...
}
```
**Just copy everything inside the file and paste it as the value!**

### 2. Connect Repository to Render

1. **Log into Render**
   - Go to https://dashboard.render.com
   - Sign in with GitHub/GitLab

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your repository
   - Select the repository containing SIFT backend

3. **Configure Service Settings**
   - **Name:** `sift-api` (or your preferred name)
   - **Root Directory:** `backend` (important!)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Choose Free tier for testing (upgrade for production)

### 3. Set Environment Variables

Go to **Environment** tab and add:

#### Required Variables:

```
GOOGLE_API_KEY=your_gemini_api_key_here
GOOGLE_SEARCH_API_KEY=your_search_api_key_here
GOOGLE_SEARCH_CX=your_custom_search_engine_id
FACT_CHECK_API_KEY=your_fact_check_api_key
GOOGLE_CREDENTIALS_JSON=<paste entire JSON file contents here>
```
**Important:** Open your downloaded JSON file, copy EVERYTHING (all lines), and paste it as the value.
**Example:** `{"type":"service_account","project_id":"my-project","private_key":"-----BEGIN...","client_email":"service@project.iam.gserviceaccount.com",...}`
```

**Important for GOOGLE_CREDENTIALS_JSON:**
- Copy the ENTIRE JSON file content
- Paste it as a single value (Render supports multiline)
- Keep all quotes and formatting exactly as in the JSON file

#### Optional Variables:

```
CORS_ORIGINS=https://your-app.netlify.app
SIFT_GEMINI_MODEL=gemini-2.0-flash
GEMINI_TEMPERATURE=0.1
CACHE_TTL=3600
HOST=0.0.0.0
```

### 4. Deploy

1. Click "Create Web Service"
2. Render will:
   - Clone your repository
   - Install dependencies
   - Start the application
3. Wait for deployment to complete (usually 2-5 minutes)
4. Your API will be available at: `https://your-service-name.onrender.com`

### 5. Verify Deployment

1. **Check Health Endpoint**
   ```bash
   curl https://your-service-name.onrender.com/
   ```

2. **Test API Endpoint**
   ```bash
   curl -X POST https://your-service-name.onrender.com/api/v1/analyze \
     -H "Content-Type: application/json" \
     -d '{"text": "Test claim"}'
   ```

3. **Check Logs**
   - Go to Render dashboard → Logs
   - Look for any errors or warnings

## Configuration Files

Render will automatically detect `render.yaml` if present in root directory. However, you can configure everything via the dashboard too.

## Auto-Deployment

By default, Render deploys automatically on every push to the main branch.

To disable:
- Go to Settings → Build & Deploy
- Toggle "Auto-Deploy" off

## Updating Environment Variables

1. Go to Environment tab
2. Edit or add variables
3. Save changes
4. Render will automatically restart the service

## Monitoring

- **Logs:** View real-time logs in Render dashboard
- **Metrics:** CPU, Memory, Response time graphs
- **Alerts:** Set up email alerts for deployment failures

## Troubleshooting

### Build Fails

**Issue:** `pip install` fails
- Check `requirements.txt` has all dependencies
- Verify Python version (Render uses Python 3.11 by default)

**Issue:** Import errors
- Verify Root Directory is set to `backend`
- Check all dependencies are in `requirements.txt`

### Service Won't Start

**Issue:** Port binding errors
- Ensure start command uses `$PORT` variable
- Verify `--host 0.0.0.0` is set

**Issue:** Environment variable errors
- Check all required env vars are set
- Verify `GOOGLE_CREDENTIALS_JSON` is valid JSON

### Translation Service Not Working

**Issue:** Authentication errors
- Verify `GOOGLE_CREDENTIALS_JSON` is set correctly
- Check JSON is complete (not truncated)
- Ensure service account has Translation API enabled

### CORS Errors

**Issue:** Frontend can't connect
- Add frontend URL to `CORS_ORIGINS` env var
- Format: `https://your-app.netlify.app` (comma-separated for multiple)
- Restart service after updating

### Cold Start Issues

Render free tier services spin down after 15 minutes of inactivity:
- First request may take 30-60 seconds (cold start)
- Subsequent requests are fast
- Upgrade to paid tier for always-on service

## Production Checklist

- [ ] All environment variables set correctly
- [ ] Health endpoint responds
- [ ] Text analysis endpoint works
- [ ] URL analysis endpoint works
- [ ] CORS configured for frontend domain
- [ ] Logs show no errors
- [ ] Service stays running (or handles cold starts gracefully)

## Cost Considerations

**Free Tier:**
- 750 hours/month free
- Services spin down after 15min inactivity
- Sleeps and wakes on first request

**Paid Tier (Starter - $7/month):**
- Always-on service
- Faster cold starts
- Better for production

## Security Notes

- Never commit API keys to repository
- Use Render's environment variables for all secrets
- Enable HTTPS (automatic on Render)
- Set appropriate CORS origins (don't use `*` in production)

