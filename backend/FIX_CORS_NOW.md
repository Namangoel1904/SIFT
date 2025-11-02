# Quick CORS Fix for Render

## Immediate Solution (Temporary)

If you need to get things working RIGHT NOW, set this environment variable in Render:

**In Render Dashboard → Your Service → Environment:**
- **Key:** `ALLOW_ALL_ORIGINS`
- **Value:** `true`
- Click **Save**

**⚠️ WARNING:** This allows ALL domains to access your API. Use only for testing!

Render will restart automatically. After 1-2 minutes, CORS errors should be gone.

---

## Permanent Fix (After Testing)

Once you confirm it works, replace with proper configuration:

1. **Remove** `ALLOW_ALL_ORIGINS` (or set to `false`)

2. **Set** `CORS_ORIGINS`:
   - **Key:** `CORS_ORIGINS`
   - **Value:** `https://siftdetect.netlify.app`
   - **Important:** 
     - No quotes
     - No brackets
     - Just the URL exactly as shown
     - Include `https://`

3. **Save** → Service restarts

---

## Verify It's Working

After setting `ALLOW_ALL_ORIGINS=true`, test:

1. Visit: https://siftdetect.netlify.app
2. Try analyzing text
3. Check browser console - CORS errors should be gone

---

## Check Configuration

Visit this debug endpoint to see current CORS settings:

```
https://sift-api.onrender.com/cors-debug
```

You should see:
```json
{
  "cors_origins": ["*", ...],
  "env_cors_origins": null,
  "allow_all_origins": "true"
}
```

---

## Next Steps After Temporary Fix Works

1. ✅ Confirm CORS works with `ALLOW_ALL_ORIGINS=true`
2. ✅ Remove `ALLOW_ALL_ORIGINS`
3. ✅ Set `CORS_ORIGINS=https://siftdetect.netlify.app`
4. ✅ Test again - should still work
5. ✅ Remove debug endpoint (optional, for security)

