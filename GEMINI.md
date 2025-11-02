# Gemini Context: SIFT Project

This document provides a comprehensive overview of the SIFT project to be used as instructional context for future AI interactions.

## 1. Project Overview

SIFT is a full-stack AI-powered browser extension for real-time misinformation detection and fact-checking. Users can select text on a webpage or enter a URL to get an analysis of factual claims, verdicts, and citations from reliable sources.

### Architecture

The project is a monorepo containing two main components:

1.  **`backend/`**: A Python-based REST API server built with **FastAPI**. It orchestrates the fact-checking process by integrating with multiple external APIs.
2.  **`extension/`**: A **React-based Chrome Extension** (Manifest V3) that serves as the user interface. It communicates with the backend to request analysis and displays the results in a browser side panel.

### Core Technologies

*   **Backend**:
    *   Framework: **FastAPI**
    *   Language: **Python**
    *   Key Libraries: `pydantic` (for settings), `httpx` (for API calls), `beautifulsoup4` (for web crawling), `google-cloud-translate`.
    *   External APIs: **Google Gemini** (for claim extraction and analysis), **Google Custom Search**, **Google Fact Check Tools API**, **Google Translate API**.

*   **Frontend**:
    *   Framework: **React** (with Hooks)
    *   Build Tool: **Vite**
    *   Styling: **Tailwind CSS**
    *   Language: **JavaScript (JSX)**

## 2. Building and Running

### Backend Setup

1.  **Navigate to the directory:**
    ```bash
    cd backend
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    # Create
    python -m venv venv
    # Activate (Windows)
    venv\Scripts\activate
    # Activate (macOS/Linux)
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure environment:**
    *   Copy `env.example` to a new `.env` file.
    *   Fill in the required API keys (`GOOGLE_API_KEY`, `GOOGLE_SEARCH_API_KEY`, etc.).
    *   Set the `GOOGLE_APPLICATION_CREDENTIALS` variable to the path of your service account JSON file.
5.  **Run the server:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

### Extension (Frontend) Setup

1.  **Navigate to the directory:**
    ```bash
    cd extension
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Build the extension for development (with hot reload):**
    ```bash
    npm run dev
    ```
4.  **Build the extension for production:**
    ```bash
    npm run build
    ```
5.  **Load the extension in Chrome:**
    *   Open Chrome and navigate to `chrome://extensions/`.
    *   Enable "Developer mode".
    *   Click "Load unpacked" and select the `extension/dist` directory.

## 3. Development Conventions

### Backend

*   **Configuration**: All configuration, API keys, and secrets are managed in `backend/app/config.py` using `pydantic-settings` and loaded from the `backend/.env` file. Do not hardcode credentials.
*   **Service Layer**: Business logic is abstracted into services within the `backend/app/services/` directory (e.g., `FactCheckService`, `LLMAnalyzer`, `TranslationService`).
*   **Asynchronous Code**: The application uses `async/await` for all I/O-bound operations, primarily API calls made with `httpx`.
*   **Error Handling**: Services should handle potential errors gracefully (e.g., API failures, crawling issues) and not crash the application. Custom exceptions or logging warnings are preferred.

### Frontend

*   **Component-Based**: The UI is built with reusable React functional components located in `extension/ui/components/`.
*   **State Management**: Component state is managed with React Hooks (`useState`, `useEffect`).
*   **Communication**: The React UI (in the side panel) communicates with the `background.js` service worker via `chrome.storage` listeners and `window.postMessage`. The background script is responsible for all communication with the backend API.
*   **Styling**: Utility-first styling is handled by **Tailwind CSS**.

### Git & Version Control

*   **Secrets**: Never commit sensitive files or credentials to the repository. The root `.gitignore` file is configured to ignore the `credentials/` directory and `.env` files.
*   **Default Branch**: The primary branch for this repository is `main`.
