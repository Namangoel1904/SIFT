# Quick Start Guide

Get SIFT up and running in 10 minutes!

## Prerequisites Checklist

- [ ] Python 3.11+ installed
- [ ] Node.js 16+ installed
- [ ] Google Gemini API key
- [ ] Google Custom Search API key + Search Engine ID
- [ ] Fact Check Tools API key

## Step 1: Backend Setup (5 minutes)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
# Windows:
copy env.example .env
# macOS/Linux:
cp env.example .env

# Edit .env file with your API keys (see Step 2 below)
# Then run server:
uvicorn app.main:app --reload
```

✅ Backend running at `http://localhost:8000`

## Step 2: Configure API Keys

Edit `backend/.env` file with your API keys:

```env
GOOGLE_API_KEY=AIzaSyC...your_gemini_key
GOOGLE_SEARCH_API_KEY=AIzaSyD...your_search_key
GOOGLE_SEARCH_CX=your_search_engine_id
FACT_CHECK_API_KEY=AIzaSyD...your_factcheck_key
SIFT_GEMINI_MODEL=gemini-2.0-flash
GEMINI_TEMPERATURE=0.1
CACHE_TTL=3600
```

## Step 3: Extension Setup (3 minutes)

```bash
# In a NEW terminal (keep backend running)
cd extension

# Install dependencies
npm install

# Build extension
npm run build
```

✅ Extension built in `extension/dist/` folder

## Step 4: Load Extension in Chrome (2 minutes)

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top-right)
3. Click "Load unpacked"
4. Navigate to `extension/dist` folder and select it
5. ✅ Extension loaded!

## Step 5: Test It!

### Test Home Screen:
- Click SIFT extension icon → Sidebar opens with Home Screen

### Test URL Analysis:
- Enter a URL in Home Screen → Click "Analyze" → See results

### Test Text Analysis:
- Highlight text on any webpage → Right-click → "Analyze with SIFT" → See results

## Verify Everything Works

1. **Backend Health Check:**
   ```
   http://localhost:8000/api/v1/health
   ```
   Should return: `{"status": "healthy"}`

2. **Extension Icon:**
   - Should appear in Chrome toolbar
   - Click to open sidebar

3. **Context Menu:**
   - Right-click on selected text
   - Should see "Analyze with SIFT" option

## Troubleshooting

**Backend won't start?**
- Activate virtual environment first
- Check Python version: `python --version` (should be 3.11+)
- Verify all dependencies installed: `pip list`

**Extension won't load?**
- Check `dist/` folder exists after build
- Verify Node.js version: `node --version` (should be 16+)
- Check Chrome console for errors (F12)

**Analysis fails?**
- Verify backend is running: `curl http://localhost:8000/api/v1/health`
- Check API keys in `backend/.env`
- Check browser console (F12) for network errors

## Need More Help?

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed setup instructions with troubleshooting.

## Next Steps

- Read [README.md](README.md) for project overview
- Check [docs/architecture.md](docs/architecture.md) for system design
- See [docs/api_contract.md](docs/api_contract.md) for API details

