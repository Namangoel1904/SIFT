# 🚀 Start Here: Deploy SIFT in 15 Minutes

## What You'll Deploy

- **Backend API** → Render (Python/FastAPI)
- **Frontend Web App** → Netlify (React/Vite)

## Prerequisites

✅ GitHub repository with SIFT code  
✅ API keys ready (see below)  
✅ 15 minutes of time

---

## Step 1: Deploy Backend (Render) ⚙️

### 1.1 Create Render Account
- Go to https://render.com
- Sign up (free tier is fine)

### 1.2 Create Web Service
1. Dashboard → **New +** → **Web Service**
2. Connect GitHub → Select your SIFT repo
3. Settings:
   ```
   Name: sift-api
   Root Directory: backend
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
4. Click **Create Web Service**

### 1.3 Add Environment Variables
Go to **Environment** tab, add:

| Variable | Value | Where to Get |
|----------|-------|--------------|
| `GOOGLE_API_KEY` | Your key | https://makersuite.google.com/app/apikey |
| `GOOGLE_SEARCH_API_KEY` | Your key | Google Cloud Console |
| `GOOGLE_SEARCH_CX` | Your CX ID | Google Custom Search |
| `FACT_CHECK_API_KEY` | Your key | Google Fact Check Tools API |
| `GOOGLE_CREDENTIALS_JSON` | Full JSON | Google Cloud Service Account |

**For GOOGLE_CREDENTIALS_JSON:**
- Download service account JSON from Google Cloud
- Copy entire file content
- Paste as environment variable value

### 1.4 Wait & Get URL
- Wait 2-5 minutes for deployment
- **Copy your backend URL** (e.g., `https://sift-api-abc123.onrender.com`)
- **Test it:** Visit the URL in browser, should see JSON response

---

## Step 2: Deploy Frontend (Netlify) 🌐

### 2.1 Create Netlify Account
- Go to https://netlify.com
- Sign up (free tier is fine)

### 2.2 Create New Site
1. **Add new site** → **Import an existing project**
2. Connect GitHub → Select your SIFT repo
3. Build settings:
   ```
   Base directory: web
   Build command: npm install && npm run build
   Publish directory: web/dist
   ```
4. Click **Deploy site**

### 2.3 Add Environment Variable
1. Site settings → **Environment variables**
2. Add:
   ```
   Key: VITE_API_URL
   Value: https://your-backend-url.onrender.com
   ```
   (Use the URL from Step 1.4)

### 2.4 Trigger Redeploy
- After adding env var, go to **Deploys**
- Click **Trigger deploy** → **Deploy site**
- Wait 1-2 minutes
- **Copy your frontend URL** (e.g., `https://sift-app-xyz.netlify.app`)

---

## Step 3: Connect Them Together 🔗

### 3.1 Update Backend CORS
1. Back to Render dashboard
2. Your service → **Environment** tab
3. Find `CORS_ORIGINS` (or add it if missing)
4. Set value to: `https://your-frontend-url.netlify.app`
5. Save → Service auto-restarts

### 3.2 Test Everything
1. Visit your Netlify URL
2. Try analyzing text: "The Earth is flat"
3. Check browser console (F12) for errors
4. If working → 🎉 **You're done!**

---

## 🔍 Troubleshooting

### Frontend shows errors
- ✅ Check `VITE_API_URL` is set correctly
- ✅ Verify backend URL is accessible
- ✅ Check browser console for specific errors

### Backend returns errors
- ✅ Check all environment variables are set
- ✅ View Render logs for error details
- ✅ Test backend directly: `curl https://your-backend.onrender.com/`

### CORS errors
- ✅ Verify `CORS_ORIGINS` includes Netlify URL
- ✅ No trailing slash in URLs
- ✅ Restart backend after updating CORS

---

## ✅ Success Checklist

- [ ] Backend URL responds to health check
- [ ] Frontend loads without errors
- [ ] Can submit text for analysis
- [ ] Can submit URL for analysis
- [ ] Results display correctly
- [ ] No CORS errors in console

---

## 📚 More Help

- **Detailed guides:** See `DEPLOYMENT_GUIDE.md`
- **Backend issues:** See `backend/DEPLOY_RENDER.md`
- **Frontend issues:** See `web/DEPLOY_NETLIFY.md`
- **Quick reference:** See `QUICK_DEPLOY.md`

---

## 🎯 Your URLs After Deployment

- **Frontend:** `https://your-app.netlify.app`
- **Backend:** `https://your-api.onrender.com`
- **API Docs:** `https://your-api.onrender.com/docs`

**Save these for future reference!**

---

## Next Steps

1. ✅ Test all features
2. ✅ Share your deployment URL
3. ✅ Set up custom domain (optional)
4. ✅ Monitor logs for any issues

**Happy Deploying! 🚀**

