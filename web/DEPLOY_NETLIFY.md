# SIFT Frontend - Netlify Deployment Guide

## Prerequisites

1. Netlify account (sign up at https://www.netlify.com)
2. GitHub/GitLab/Bitbucket account (to connect repository)
3. Backend API URL (from Render deployment)

## Step-by-Step Deployment

### Option 1: Deploy via Netlify Dashboard (Recommended for First Time)

1. **Push Code to Repository**
   - Ensure your code is pushed to GitHub/GitLab/Bitbucket
   - Make sure `web/` folder contains all frontend files

2. **Log into Netlify**
   - Go to https://app.netlify.com
   - Sign in with your GitHub/GitLab account

3. **Create New Site**
   - Click "Add new site" → "Import an existing project"
   - Connect to your repository
   - Select the repository with SIFT code

4. **Configure Build Settings**
   - **Base directory:** `web`
   - **Build command:** `npm install && npm run build`
   - **Publish directory:** `web/dist`
   
   Netlify should auto-detect these from `netlify.toml`, but verify them.

5. **Set Environment Variables**
   - Go to Site settings → Environment variables
   - Add:
     - Key: `VITE_API_URL`
     - Value: `https://your-render-app.onrender.com` (your Render backend URL)

6. **Deploy**
   - Click "Deploy site"
   - Wait for build to complete
   - Your site will be live at `https://your-site-name.netlify.app`

### Option 2: Deploy via Netlify CLI

1. **Install Netlify CLI**
   ```bash
   npm install -g netlify-cli
   ```

2. **Login to Netlify**
   ```bash
   netlify login
   ```

3. **Navigate to Web Directory**
   ```bash
   cd web
   ```

4. **Initialize and Deploy**
   ```bash
   netlify init
   netlify deploy --prod
   ```

5. **Set Environment Variables**
   ```bash
   netlify env:set VITE_API_URL https://your-render-app.onrender.com
   ```

## Environment Variables

### Required

- `VITE_API_URL` - Your Render backend URL (e.g., `https://sift-api.onrender.com`)

### Optional

- None currently required

## Build Configuration

Netlify automatically uses `netlify.toml` configuration:
- Build command: `npm run build`
- Publish directory: `dist`
- SPA routing: All routes redirect to `index.html`

## Updating the Site

### Automatic Deployment
- Every push to main branch automatically triggers a new deployment
- Netlify creates preview deployments for pull requests

### Manual Deployment
- Use Netlify dashboard → "Trigger deploy" → "Deploy site"
- Or use CLI: `netlify deploy --prod`

## Custom Domain

1. Go to Site settings → Domain management
2. Click "Add custom domain"
3. Follow instructions to configure DNS

## Troubleshooting

### Build Fails

1. Check build logs in Netlify dashboard
2. Common issues:
   - Missing dependencies: Ensure `package.json` has all dependencies
   - Environment variables: Check `VITE_API_URL` is set correctly
   - Node version: Netlify uses Node 18 by default

### CORS Errors

- Ensure backend `CORS_ORIGINS` includes your Netlify URL
- Check backend logs for CORS errors

### API Not Connecting

- Verify `VITE_API_URL` environment variable is set correctly
- Check backend is deployed and running
- Test backend URL directly: `curl https://your-backend.onrender.com/`

## Post-Deployment Checklist

- [ ] Site loads correctly
- [ ] Can submit text analysis
- [ ] Can submit URL analysis
- [ ] Results page displays correctly
- [ ] No console errors in browser
- [ ] CORS working (no CORS errors in console)

