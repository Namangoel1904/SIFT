# Quick Deployment Checklist

Follow these steps in order to deploy SIFT.

## 🚀 Backend (Render) - Do This First

1. **Go to Render Dashboard** → https://dashboard.render.com
2. **New +** → **Web Service**
3. **Connect Repository** → Select your SIFT repo
4. **Settings:**
   - Root Directory: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. **Environment Variables** (Environment tab):
   ```
   GOOGLE_API_KEY=...
   GOOGLE_SEARCH_API_KEY=...
   GOOGLE_SEARCH_CX=...
   FACT_CHECK_API_KEY=...
   GOOGLE_CREDENTIALS_JSON={...full JSON...}
   CORS_ORIGINS=https://your-app.netlify.app (set after frontend deploys)
   ```
6. **Create Web Service** → Wait 2-5 min
7. **Copy Backend URL** → Save this! (e.g., `https://sift-api-xyz.onrender.com`)

## 🌐 Frontend (Netlify) - Do This Second

1. **Go to Netlify Dashboard** → https://app.netlify.com
2. **Add new site** → **Import an existing project**
3. **Connect Repository** → Select your SIFT repo
4. **Build Settings:**
   - Base directory: `web`
   - Build command: `npm install && npm run build`
   - Publish directory: `web/dist`
5. **Environment Variables** (Site settings → Environment):
   ```
   VITE_API_URL=https://your-backend-url.onrender.com
   ```
   (Use the URL from step 7 above)
6. **Deploy site** → Wait 1-2 min
7. **Copy Frontend URL** → (e.g., `https://sift-app-12345.netlify.app`)

## 🔄 Final Step: Update Backend CORS

1. **Back to Render** → Your service → Environment
2. **Update CORS_ORIGINS:**
   ```
   https://your-frontend-url.netlify.app
   ```
3. **Save** → Service auto-restarts

## ✅ Test

1. Visit your Netlify URL
2. Try analyzing some text
3. Check browser console for errors
4. Done! 🎉

---

**Need detailed instructions?** See `DEPLOYMENT_GUIDE.md`

