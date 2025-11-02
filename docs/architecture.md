# SIFT Architecture

## Overview

SIFT (AI Misinformation Prevention & Fact-Checking) is a full-stack browser extension that helps users identify and verify misinformation in online content. The system consists of a Chrome extension (frontend) and a FastAPI backend that performs AI-powered fact-checking.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Chrome Extension                          │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Content      │  │ Background   │  │ React UI        │  │
│  │ Script       │◄─┤ Service      │◄─┤ (Pop-up)        │  │
│  │              │  │ Worker       │  │                 │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ HTTP/HTTPS
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              API Routes (/api/v1)                     │  │
│  │  - POST /analyze/text                                 │  │
│  │  - POST /analyze/url                                  │  │
│  │  - GET /health                                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                  │
│  ┌────────────────────────▼──────────────────────────────┐  │
│  │            FactCheckService (Orchestrator)            │  │
│  └──────────────────────────────────────────────────────┘  │
│         │         │         │         │         │           │
│    ┌────▼────┐ ┌──▼───┐ ┌──▼──┐ ┌──▼───┐ ┌───▼───┐        │
│    │ Claim   │ │Query │ │Search│ │Crawl │ │  LLM │        │
│    │Extractor│ │Gen.  │ │Service│ │ er   │ │Analyzer│     │
│    └─────────┘ └──────┘ └──────┘ └──────┘ └───────┘        │
└─────────────────────────────────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
    Google Search    Fact-check Sites   OpenAI API
        API          (Snopes, etc.)    (GPT-4)
```

## Components

### Chrome Extension (Frontend)

#### 1. **Content Script** (`content-script.js`)
- Injected into web pages
- Monitors text selection
- Shows "SIFT Check" button on text selection
- Extracts page content for analysis
- Handles keyboard shortcuts (Ctrl+Shift+S)

#### 2. **Background Service Worker** (`background.js`)
- Handles communication between content script and popup
- Manages API calls to backend
- Stores configuration (API URL)
- Message passing between extension components

#### 3. **React UI** (`ui/`)
- Popup interface built with React and Vite
- TailwindCSS for styling
- Components:
  - **App.jsx**: Main application component
  - **ClaimResultCard.jsx**: Displays individual fact-check results
  - **Loader.jsx**: Loading state component
  - **ErrorState.jsx**: Error handling component

### FastAPI Backend

#### 1. **API Routes** (`routes/analyze.py`)
- RESTful endpoints for text and URL analysis
- Request validation using Pydantic models
- Error handling and response formatting

#### 2. **Services Layer**

**FactCheckService** (`services/factcheck_service.py`)
- Main orchestrator that coordinates all services
- Implements the fact-checking workflow:
  1. Extract claims from text
  2. Generate search queries for each claim
  3. Search fact-checking sources
  4. Crawl and fetch source content
  5. Use LLM to fact-check claims
  6. Aggregate and return results

**ClaimExtractor** (`services/claim_extractor.py`)
- Extracts factual claims from text using LLM
- Falls back to pattern-based extraction
- Categorizes claims (statistical, historical, scientific, etc.)

**QueryGenerator** (`services/query_generator.py`)
- Generates optimized search queries for fact-checking
- Uses LLM to create effective search terms
- Includes fact-checking site targeting

**SearchService** (`services/search_service.py`)
- Integrates with Google Custom Search API
- Filters and prioritizes fact-checking sources
- Fallback search methods

**Crawler** (`services/crawler.py`)
- Fetches web page content
- Extracts text from HTML
- Handles timeouts and retries
- Parses metadata (title, description)

**LLMAnalyzer** (`services/llm_analyzer.py`)
- Interfaces with OpenAI API (GPT-4)
- Handles JSON and text responses
- Performs fact-checking analysis
- Confidence scoring

**Utils** (`services/utils.py`)
- Text cleaning and normalization
- URL validation and normalization
- HTML parsing helpers
- Data deduplication

## Data Flow

### Text Analysis Flow

1. User selects text on webpage → Content script captures selection
2. Content script sends message → Background service worker
3. Background worker → Calls FastAPI `/analyze/text` endpoint
4. Backend processes:
   - Extract claims → ClaimExtractor
   - For each claim:
     - Generate queries → QueryGenerator
     - Search sources → SearchService
     - Fetch content → Crawler (optional)
     - Fact-check → LLMAnalyzer
5. Results returned → Extension popup displays results

### URL Analysis Flow

1. User enters URL in popup → React UI
2. UI calls FastAPI `/analyze/url` endpoint
3. Backend:
   - Fetch URL content → Crawler
   - Extract text → Extract text from HTML
   - Follow text analysis flow (steps 4-5 above)

## Technology Stack

### Frontend
- **Manifest V3**: Chrome extension API
- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **TailwindCSS**: Utility-first CSS framework

### Backend
- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation
- **httpx**: Async HTTP client
- **BeautifulSoup4**: HTML parsing
- **OpenAI API**: LLM integration (GPT-4)

## Security Considerations

1. **API Keys**: Stored in environment variables, never in code
2. **CORS**: Configured to allow extension origins only
3. **Content Security Policy**: Extension uses Manifest V3 CSP
4. **Input Validation**: All inputs validated using Pydantic models
5. **Error Handling**: Graceful error handling prevents information leakage

## Scalability

- **Async/Await**: All I/O operations are asynchronous
- **Concurrent Requests**: Multiple claims processed concurrently
- **Rate Limiting**: Can be added via middleware
- **Caching**: Can cache search results and fact-checks
- **Database**: Can add persistent storage for results

## Future Enhancements

1. **Database Integration**: Store fact-check history
2. **User Accounts**: Save preferences and history
3. **Additional LLM Providers**: Support for Claude, Gemini, etc.
4. **Real-time Updates**: WebSocket support for long-running analysis
5. **Browser Compatibility**: Extend to Firefox, Edge
6. **Mobile Support**: Create mobile app versions
7. **Community Features**: User-contributed fact-checks

