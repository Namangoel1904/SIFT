# Extension Download Setup

## Option 1: Google Drive (Recommended)

### Step 1: Upload Extension Zip to Google Drive

1. Zip your extension folder (`extension/dist` or the built extension)
2. Upload to Google Drive
3. Right-click → **Get link**
4. Set permission to **"Anyone with the link can view"**

### Step 2: Get Direct Download Link

1. Copy the shareable link (looks like):
   ```
   https://drive.google.com/file/d/FILE_ID/view?usp=sharing
   ```

2. Extract the `FILE_ID` (the long string between `/d/` and `/view`)

3. Create direct download URL (with `confirm=t` to bypass virus scan):
   ```
   https://drive.google.com/uc?export=download&confirm=t&id=FILE_ID
   ```
   
   **Important:** The `confirm=t` parameter is required for zip files and other files that trigger Google Drive's virus scan warning.

### Step 3: Set in Netlify Environment Variable

1. Go to Netlify Dashboard → Your Site → **Environment variables**
2. Add:
   - **Key:** `VITE_EXTENSION_DOWNLOAD_URL`
   - **Value:** `https://drive.google.com/uc?export=download&id=YOUR_FILE_ID`
3. **Trigger redeploy** after adding

---

## Option 2: Direct File Hosting (Netlify Public Folder)

### Step 1: Add File to Public Folder

1. Place `sift-extension.zip` in `web/public/` directory
2. Commit and push:
   ```bash
   git add web/public/sift-extension.zip
   git commit -m "Add extension zip file"
   git push
   ```

### Step 2: Update Component (Already Done)

The component will automatically use `/sift-extension.zip` if no environment variable is set.

---

## Option 3: External CDN/File Hosting

Use any file hosting service:

1. Upload zip file to:
   - Dropbox (get direct link)
   - GitHub Releases
   - AWS S3
   - Any CDN

2. Set `VITE_EXTENSION_DOWNLOAD_URL` in Netlify to the direct download URL

---

## Quick Google Drive Setup

1. **Upload** `sift-extension.zip` to Google Drive
2. **Right-click** → **Get link** → **Change to "Anyone with the link"**
3. **Copy link** (e.g., `https://drive.google.com/file/d/1ABC123xyz456/view?usp=sharing`)
4. **Extract ID**: `1ABC123xyz456`
5. **Create URL**: `https://drive.google.com/uc?export=download&confirm=t&id=1ABC123xyz456`
   (The `confirm=t` parameter is important for large files)
6. **Set in Netlify**: `VITE_EXTENSION_DOWNLOAD_URL` = the URL from step 5
7. **Redeploy** Netlify site

---

## Testing

After setup:
1. Visit `/extension` page
2. Click "Download Extension" button
3. Should download or open the zip file

---

## Troubleshooting

### Google Drive says "Virus scan warning"

**Solution:** Use a service account or upload to GitHub Releases instead

### Download doesn't start

**Solution:** 
- Make sure link has `export=download` parameter
- Check file permissions (should be public)
- Try opening link directly in browser first

### File too large for Google Drive

**Solution:**
- Use GitHub Releases (unlimited size)
- Use AWS S3 or similar CDN
- Split into multiple parts (not recommended)

