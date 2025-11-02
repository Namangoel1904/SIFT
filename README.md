# SIFT - AI Misinformation Prevention & Fact-Checking

A full-stack browser extension that uses AI to detect and fact-check misinformation in online content.

## Features

- 🔍 **Real-time Fact-Checking**: Select text on any webpage and get instant fact-check results
- 🤖 **AI-Powered Analysis**: Uses GPT-4 to extract claims and verify them
- 🌐 **Web Crawling**: Fetches and analyzes content from URLs
- 📊 **Detailed Results**: Confidence scores, explanations, and source citations
- 🎨 **Modern UI**: Beautiful React interface with TailwindCSS

## Architecture

- **Frontend**: Chrome Extension (Manifest V3) with React + Vite + TailwindCSS
- **Backend**: FastAPI with Python, integrating OpenAI API and Google Search API

## Quick Start

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the `backend` directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here
HOST=0.0.0.0
PORT=8000
```

5. Run the backend:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Extension Setup

1. Navigate to the extension directory:
```bash
cd extension
```

2. Install dependencies:
```bash
npm install
```

3. Build the extension:
```bash
npm run build
```

4. Load the extension in Chrome:
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked"
   - Select the `extension/dist` directory (after build)

5. For development with hot reload:
```bash
npm run dev
```

### Using Docker (Backend)

```bash
cd backend
docker build -t sift-backend .
docker run -p 8000:8000 --env-file .env sift-backend
```

## Usage

### Via Extension Popup

1. Click the SIFT extension icon
2. Paste text or enter a URL
3. Click "Analyze Text" or "Analyze URL"
4. View fact-check results

### Via Text Selection

1. Select text on any webpage
2. A "🔍 SIFT Check" button will appear
3. Click the button to analyze
4. Results appear in the extension popup

### Keyboard Shortcut

- **Ctrl+Shift+S**: Analyze selected text (or entire page if no selection)

## Project Structure

```
/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration settings
│   │   ├── routes/
│   │   │   └── analyze.py       # API routes
│   │   └── services/
│   │       ├── claim_extractor.py
│   │       ├── query_generator.py
│   │       ├── search_service.py
│   │       ├── factcheck_service.py
│   │       ├── crawler.py
│   │       ├── llm_analyzer.py
│   │       └── utils.py
│   ├── requirements.txt
│   └── Dockerfile
├── extension/
│   ├── manifest.json
│   ├── src/
│   │   ├── background.js        # Service worker
│   │   └── content-script.js    # Content script
│   ├── ui/
│   │   ├── index.html
│   │   ├── index.jsx
│   │   ├── App.jsx
│   │   └── components/
│   │       ├── ClaimResultCard.jsx
│   │       ├── Loader.jsx
│   │       └── ErrorState.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
└── docs/
    ├── architecture.md
    └── api_contract.md
```

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

For detailed API documentation, see [docs/api_contract.md](docs/api_contract.md)

## Configuration

### Backend Environment Variables

- `OPENAI_API_KEY`: Required for LLM analysis
- `GOOGLE_API_KEY`: Optional, for Google Custom Search
- `GOOGLE_SEARCH_ENGINE_ID`: Optional, for Google Custom Search
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)

### Extension Configuration

The extension connects to the backend API. By default, it uses `http://localhost:8000`. You can change this in the extension's background script or add a settings UI.

## Development

### Backend Development

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Extension Development

```bash
cd extension
npm run dev
```

Then load the extension from the `dist` directory after building.

## Testing

### Test the Backend

```bash
curl -X POST "http://localhost:8000/api/v1/analyze/text" \
  -H "Content-Type: application/json" \
  -d '{"text": "The sky is blue.", "url": null}'
```

### Test the Extension

1. Load the extension in Chrome
2. Visit any webpage
3. Select text and click the SIFT button
4. Or open the popup and paste text

## Troubleshooting

### Backend Issues

- **OpenAI API errors**: Check your API key and quota
- **Google Search errors**: Ensure API key and Search Engine ID are set
- **Import errors**: Make sure all dependencies are installed

### Extension Issues

- **Popup not opening**: Check that the extension is loaded and enabled
- **API connection errors**: Verify backend is running and URL is correct
- **Build errors**: Run `npm install` and check Node.js version (v16+)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source. See LICENSE file for details.

## Acknowledgments

- OpenAI for GPT-4 API
- Google for Custom Search API
- FastAPI for the excellent Python framework
- React and TailwindCSS communities

