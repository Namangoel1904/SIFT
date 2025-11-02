# CORS Configuration for Render

## Problem

If you see CORS errors like:
```
Access to fetch at 'https://sift-api.onrender.com/api/v1/analyze' from origin 'https://siftdetect.netlify.app' has been blocked by CORS policy
```

This means your backend hasn't been configured to allow requests from your Netlify frontend.

## Solution

### Step 1: Get Your Netlify URL

Your frontend URL is: `https://siftdetect.netlify.app`

### Step 2: Set CORS_ORIGINS in Render

1. **Go to Render Dashboard**
   - https://dashboard.render.com
   - Click on your backend service (`sift-api`)

2. **Go to Environment Tab**
   - Click on **Environment** in the left sidebar

3. **Add or Update CORS_ORIGINS**
   - Find `CORS_ORIGINS` in the environment variables list
   - If it doesn't exist, click **Add Environment Variable**
   - **Key:** `CORS_ORIGINS`
   - **Value:** `https://siftdetect.netlify.app`
   - **Important:** Just the URL, no quotes, no brackets, no JSON format!
   - Click **Save Changes**

4. **Service Auto-Restarts**
   - Render will automatically restart your service
   - Wait 1-2 minutes for restart

### Step 3: Verify

Test if CORS is working:

1. **Visit your Netlify site:** https://siftdetect.netlify.app
2. **Try analyzing some text**
3. **Check browser console** - CORS errors should be gone

## Multiple Domains

If you need to allow multiple domains, separate them with commas:

```
https://siftdetect.netlify.app,https://another-domain.com
```

## Troubleshooting

### Still Getting CORS Errors?

1. **Check the exact URL**
   - Make sure `CORS_ORIGINS` matches your Netlify URL exactly
   - Include `https://` (don't forget the protocol)
   - No trailing slash

2. **Verify Service Restarted**
   - Check Render logs to confirm restart completed
   - Look for "Started server process" message

3. **Test Backend Directly**
   ```bash
   curl -X OPTIONS https://sift-api.onrender.com/api/v1/analyze \
     -H "Origin: https://siftdetect.netlify.app" \
     -H "Access-Control-Request-Method: POST" \
     -v
   ```
   Should see `Access-Control-Allow-Origin: https://siftdetect.netlify.app` in response

4. **Check Render Logs**
   - Go to Render → Your Service → Logs
   - Look for any CORS-related errors or warnings

## Quick Reference

**Render Environment Variable:**
```
CORS_ORIGINS=https://siftdetect.netlify.app
```

**After setting:**
- Service restarts automatically
- Changes take effect in 1-2 minutes
- No code changes needed

