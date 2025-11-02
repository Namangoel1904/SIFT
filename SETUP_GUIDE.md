# Complete SIFT Setup Guide

This guide will walk you through setting up and running the SIFT extension from scratch.

## Prerequisites

- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Node.js 16+** and npm ([Download](https://nodejs.org/))
- **Google Chrome** or Chromium-based browser
- **API Keys** (see below)

---

## Step 1: Get Required API Keys

### A. Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key (starts with `AIza...`)

### B. Google Custom Search API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable **Custom Search API**:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Custom Search API"
   - Click "Enable"
4. Create API Key:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy the API key
5. Create Custom Search Engine:
   - Go to [Programmable Search Engine](https://programmablesearchengine.google.com/controlpanel/create)
   - Click "Add"
   - Enter any name (e.g., "SIFT Search")
   - Choose "Search the entire web"
   - Click "Create"
   - Copy the **Search Engine ID** (CX)

### C. Fact Check Tools API

1. Go to [Google Fact Check Tools API](https://developers.google.com/fact-check/tools/api)
2. Click "Get Started"
3. Enable the API in Google Cloud Console
4. Create an API key (can use the same as Custom Search API or create separate)

---

## Step 2: Backend Setup

### 2.1 Navigate to Backend Directory

```bash
cd backend
```

### 2.2 Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2.3 Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI
- Uvicorn
- httpx
- BeautifulSoup4
- PyPDF2
- pdfplumber
- And other dependencies

### 2.4 Configure Environment Variables

1. Copy the example file:
   ```bash
   # Windows
   copy env.example .env

   # macOS/Linux
   cp env.example .env
   ```

2. Open `.env` file and add your API keys:
   ```env
   # Google Gemini API Configuration
   GOOGLE_API_KEY=AIzaSyC...your_key_here

   # Gemini Model Configuration
   SIFT_GEMINI_MODEL=gemini-2.0-flash
   GEMINI_TEMPERATURE=0.1

   # Google Custom Search API
   GOOGLE_SEARCH_API_KEY=AIzaSyD...your_key_here
   GOOGLE_SEARCH_CX=your_search_engine_id_here

   # Fact Check Tools API
   FACT_CHECK_API_KEY=AIzaSyD...your_key_here

   # Cache Configuration
   CACHE_TTL=3600

   # Server Configuration
   HOST=0.0.0.0
   PORT=8000
   ```

3. **Important**: Replace all placeholder values with your actual API keys!

### 2.5 Start Backend Server

```bash
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

✅ **Backend is running!** Keep this terminal open.

---

## Step 3: Extension Setup

### 3.1 Open New Terminal

Open a **new terminal window** (keep backend running in the first terminal).

### 3.2 Navigate to Extension Directory

```bash
cd extension
```

### 3.3 Install Node Dependencies

```bash
npm install
```

This installs:
- React
- Vite
- TailwindCSS
- And other build dependencies

### 3.4 Build the Extension

```bash
npm run build
```

This will:
1. Build the React UI with Vite
2. Copy manifest.json and scripts to `dist/` folder
3. Prepare the extension for loading

You should see output like:
```
✓ Copied manifest.json
✓ Copied src/ directory
⚠ Icons directory not found - extension will work but may show placeholder icons
✓ Extension files copied to dist/
```

### 3.5 (Optional) Create Extension Icons

1. Create `icons/` folder in `extension/` directory:
   ```bash
   mkdir icons
   ```

2. Add three PNG files:
   - `icon16.png` (16x16 pixels)
   - `icon48.png` (48x48 pixels)
   - `icon128.png` (128x128 pixels)

3. You can create simple icons or use placeholder images for now.

---

## Step 4: Load Extension in Chrome

### 4.1 Open Chrome Extensions Page

1. Open Google Chrome
2. Navigate to `chrome://extensions/`
   - Or: Menu (⋮) > Extensions > Manage Extensions

### 4.2 Enable Developer Mode

1. Toggle "Developer mode" switch in the top-right corner
2. This enables loading unpacked extensions

### 4.3 Load the Extension

1. Click "Load unpacked" button
2. Navigate to: `D:\SIFT2.0\extension\dist`
3. Select the `dist` folder
4. Click "Select Folder"

✅ **Extension is loaded!** You should see "SIFT - AI Misinformation Prevention" in your extensions list.

---

## Step 5: Test the Extension

### Test 1: Home Screen

1. Click the SIFT extension icon in Chrome toolbar
2. Sidebar should slide in from the right
3. You should see:
   - SIFT title and logo
   - Instructions
   - URL input field

### Test 2: URL Analysis

1. In the Home Screen, paste a URL (e.g., `https://example.com/article`)
2. Click "Analyze" button
3. Wait for analysis (shows "Analyzing… Thinking critically…")
4. Results should appear with verdict, confidence, and citations

### Test 3: Text Selection Analysis

1. Visit any webpage
2. Highlight some text (at least 10 characters)
3. Right-click on the selected text
4. Click "Analyze with SIFT" in context menu
5. Sidebar opens directly to Results Screen
6. Claims should appear with fact-check results

---

## Step 6: Verify Backend Connection

### Check API Endpoint

Open browser and go to:
```
http://localhost:8000/api/v1/health
```

Should return:
```json
{
  "status": "healthy",
  "service": "SIFT API"
}
```

### Check API Docs

Visit:
```
http://localhost:8000/docs
```

You should see Swagger UI with the `/analyze` endpoint.

---

## Troubleshooting

### Backend Issues

**Problem: ModuleNotFoundError**
```bash
# Solution: Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

**Problem: API Key Errors**
- Check `.env` file exists in `backend/` directory
- Verify all API keys are correct (no extra spaces)
- Restart the backend server after changing `.env`

**Problem: Port 8000 already in use**
```bash
# Change port in .env file
PORT=8001

# Or kill process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Extension Issues

**Problem: Extension doesn't load**
- Check `dist/` folder exists after build
- Verify `manifest.json` is in `dist/` folder
- Check Chrome console for errors (F12)

**Problem: Sidebar doesn't open**
- Check content script is loaded (Chrome DevTools > Sources > Content scripts)
- Verify backend is running on `http://localhost:8000`
- Check for errors in extension background page

**Problem: Analysis fails**
- Verify backend server is running
- Check API URL in `extension/src/background.js` matches your backend
- Check browser console (F12) for network errors
- Verify API keys are set correctly

**Problem: Build errors**
```bash
# Clean and rebuild
rm -rf dist node_modules
npm install
npm run build
```

### API Key Issues

**Problem: Gemini API errors**
- Verify API key is correct
- Check API quota/limits in Google Cloud Console
- Ensure `gemini-2.0-flash` model is available in your region

**Problem: Search API errors**
- Verify Custom Search Engine ID (CX) is correct
- Check API is enabled in Google Cloud Console
- Verify search quota hasn't been exceeded

---

## Quick Start Commands Reference

### Backend (Terminal 1)
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
# Edit .env with your API keys
uvicorn app.main:app --reload
```

### Extension (Terminal 2)
```bash
cd extension
npm install
npm run build
# Then load dist/ folder in Chrome
```

---

## Production Deployment

### Backend Deployment

1. Use Docker:
   ```bash
   cd backend
   docker build -t sift-backend .
   docker run -p 8000:8000 --env-file .env sift-backend
   ```

2. Or deploy to cloud services:
   - Heroku
   - AWS Elastic Beanstalk
   - Google Cloud Run
   - DigitalOcean App Platform

### Extension Distribution

1. Build production version:
   ```bash
   npm run build
   ```

2. Create ZIP file of `dist/` folder

3. Submit to Chrome Web Store:
   - Go to [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole)
   - Upload ZIP file
   - Fill in store listing details

---

## Next Steps

- ✅ Backend running on `http://localhost:8000`
- ✅ Extension loaded in Chrome
- ✅ API keys configured
- 🎉 **Ready to fact-check!**

For more information, see:
- [README.md](README.md) - Project overview
- [docs/architecture.md](docs/architecture.md) - System architecture
- [docs/api_contract.md](docs/api_contract.md) - API documentation

