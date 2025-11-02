# SIFT Web Frontend

Web application for SIFT - Source • Investigate • Find • Trace

## Features

- 🔍 **Home Page**: Text and URL input for fact-checking
- 📊 **Results Page**: Detailed fact-check results with confidence scores
- 📦 **Extension Download**: Installation instructions and download

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env` file:
```env
VITE_API_URL=http://localhost:8000
```

3. Run development server:
```bash
npm run dev
```

4. Build for production:
```bash
npm run build
```

## Deployment

The project is configured for Netlify. The build output is in `dist/` directory.

## Brand Colors

- Primary: #0055FF
- Accent: #2ECC71
- Error: #D32F2F
- Warning: #FF9800
- Neutral: #FFFFFF

## Tech Stack

- React 18
- Vite
- TailwindCSS
- React Router

