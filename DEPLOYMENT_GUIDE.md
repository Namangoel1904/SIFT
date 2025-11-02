# SIFT Complete Deployment Guide

This guide walks you through deploying both the frontend (Netlify) and backend (Render) for the SIFT application.

## Overview

- **Frontend:** React app deployed on Netlify
- **Backend:** FastAPI app deployed on Render
- **Communication:** Frontend calls backend API via environment variable

## Prerequisites

1. ✅ GitHub/GitLab repository with SIFT code
2. ✅ Netlify account (free tier is fine)
3. ✅ Render account (free tier is fine)
4. ✅ All API keys and credentials (see below)

## Part 1: Deploy Backend to Render

### Step 1: Prepare Backend

1. **Ensure all files are committed:**
   ```bash
   git status
   git add .
   git commit -m "Prepare for Render deployment"
   git push
   ```

### Step 2: Deploy on Render

1. **Go to Render Dashboard**
   - Visit https://dashboard.render.com
   - Sign in with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your repository
   - Select your SIFT repository

3. **Configure Service:**
   ```
   Name: sift-api
   Root Directory: backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Set Environment Variables:**
   
   Go to Environment tab and add:
   
   ```
   GOOGLE_API_KEY=your_key_here
   GOOGLE_SEARCH_API_KEY=your_key_here
   GOOGLE_SEARCH_CX=your_cx_here
   FACT_CHECK_API_KEY=your_key_here
   GOOGLE_CREDENTIALS_JSON={"type":"service_account",...} (full JSON)
   CORS_ORIGINS=https://your-netlify-app.netlify.app
   ```
   
   **Getting GOOGLE_CREDENTIALS_JSON:**
   - Download service account JSON from Google Cloud Console
   - Copy entire file content
   - Paste into Render environment variable

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (2-5 minutes)
   - Note your backend URL: `https://sift-api.onrender.com` (or similar)

6. **Test Backend**
   ```bash
   # Health check
   curl https://your-backend-url.onrender.com/
   
   # Should return: {"message":"SIFT API...","version":"1.0.0"}
   ```

✅ **Backend is now live!** Copy the URL, you'll need it for frontend.

---

## Part 2: Deploy Frontend to Netlify

### Step 1: Prepare Frontend

1. **Verify web folder structure:**
   ```
   web/
   ├── src/
   ├── public/
   ├── package.json
   ├── vite.config.js
   └── netlify.toml
   ```

### Step 2: Deploy on Netlify

**Option A: Via Netlify Dashboard (Recommended)**

1. **Go to Netlify Dashboard**
   - Visit https://app.netlify.com
   - Sign in with GitHub

2. **Create New Site**
   - Click "Add new site" → "Import an existing project"
   - Connect your GitHub repository
   - Select your SIFT repository

3. **Configure Build Settings:**
   ```
   Base directory: web
   Build command: npm install && npm run build
   Publish directory: web/dist
   ```

4. **Set Environment Variables:**
   
   Go to Site settings → Environment variables:
   
   ```
   VITE_API_URL=https://your-backend-url.onrender.com
   ```
   
   **Replace `your-backend-url.onrender.com` with your actual Render backend URL!**

5. **Deploy**
   - Click "Deploy site"
   - Wait for build (1-2 minutes)
   - Your site will be live at `https://random-name-12345.netlify.app`

**Option B: Via Netlify CLI**

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Navigate to web directory
cd web

# Initialize and deploy
netlify init
netlify env:set VITE_API_URL https://your-backend-url.onrender.com
netlify deploy --prod
```

### Step 3: Update Backend CORS

1. **Go back to Render Dashboard**
2. **Update Environment Variable:**
   - Find `CORS_ORIGINS`
   - Update value to: `https://your-netlify-app.netlify.app`
   - Save (service will auto-restart)

### Step 4: Test Frontend

1. **Visit your Netlify site**
2. **Try submitting a text analysis**
3. **Check browser console for errors**
4. **Verify results display correctly**

---

## Part 3: Verification Checklist

### Backend (Render)
- [ ] Health endpoint works: `curl https://backend-url/`
- [ ] API docs accessible: `https://backend-url/docs`
- [ ] Text analysis endpoint works
- [ ] URL analysis endpoint works
- [ ] CORS headers include Netlify domain
- [ ] No errors in Render logs

### Frontend (Netlify)
- [ ] Site loads without errors
- [ ] Home page displays correctly
- [ ] Can submit text for analysis
- [ ] Can submit URL for analysis
- [ ] Results page displays correctly
- [ ] No CORS errors in browser console
- [ ] API calls succeed (check Network tab)

### Integration
- [ ] Frontend successfully connects to backend
- [ ] Analysis requests complete
- [ ] Results are displayed properly
- [ ] Error handling works (try invalid input)

---

## Troubleshooting

### Frontend can't connect to backend

**Symptoms:** CORS errors, network errors, 404s

**Solutions:**
1. Verify `VITE_API_URL` is set correctly in Netlify
2. Check backend `CORS_ORIGINS` includes Netlify URL
3. Ensure backend URL doesn't have trailing slash
4. Check browser console for specific error messages

### Backend returns 500 errors

**Symptoms:** Analysis requests fail

**Solutions:**
1. Check Render logs for error details
2. Verify all environment variables are set
3. Test backend directly with curl
4. Check API keys are valid

### Build fails on Netlify

**Symptoms:** Deployment fails

**Solutions:**
1. Check build logs in Netlify
2. Verify `package.json` has all dependencies
3. Ensure Node version is compatible (Netlify uses Node 18)
4. Check for TypeScript/lint errors

### Backend cold start issues

**Symptoms:** First request takes 30-60 seconds

**Solutions:**
- This is normal on Render free tier
- Service spins down after 15min inactivity
- Consider upgrade to paid tier for production
- Or add a keep-alive ping every 10 minutes

---

## Custom Domain Setup

### Netlify Custom Domain

1. Go to Site settings → Domain management
2. Click "Add custom domain"
3. Follow DNS configuration instructions

### Update Backend CORS

After setting custom domain:
1. Update `CORS_ORIGINS` in Render to include custom domain
2. Restart service

---

## Environment Variables Summary

### Render (Backend)
```
GOOGLE_API_KEY
GOOGLE_SEARCH_API_KEY
GOOGLE_SEARCH_CX
FACT_CHECK_API_KEY
GOOGLE_CREDENTIALS_JSON
CORS_ORIGINS
```

### Netlify (Frontend)
```
VITE_API_URL
```

---

## Next Steps

1. ✅ Both services are deployed
2. ✅ Test all functionality
3. ✅ Set up custom domain (optional)
4. ✅ Monitor logs for errors
5. ✅ Consider upgrading tiers for production use

---

## Support

- **Netlify Docs:** https://docs.netlify.com
- **Render Docs:** https://render.com/docs
- **Backend Issues:** Check `backend/DEPLOY_RENDER.md`
- **Frontend Issues:** Check `web/DEPLOY_NETLIFY.md`

---

## Quick Reference URLs

After deployment, you'll have:
- **Frontend:** `https://your-app.netlify.app`
- **Backend:** `https://your-api.onrender.com`
- **Backend Docs:** `https://your-api.onrender.com/docs`

Save these URLs for reference!

