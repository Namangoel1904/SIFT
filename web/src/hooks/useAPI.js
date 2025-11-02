// API Base URL - defaults to localhost for development
// For production, set VITE_API_URL environment variable in Netlify
const getApiBaseUrl = () => {
  const url = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  // Remove trailing slash if present to avoid double slashes
  return url.replace(/\/$/, '');
};

const API_BASE_URL = getApiBaseUrl();

export async function analyzeText(text) {
  const response = await fetch(`${API_BASE_URL}/api/v1/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Failed to analyze text' }));
    throw new Error(errorData.detail || 'Failed to analyze text');
  }

  return await response.json();
}

export async function analyzeURL(url) {
  const response = await fetch(`${API_BASE_URL}/api/v1/analyze/url`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ url }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Failed to analyze URL' }));
    throw new Error(errorData.detail || 'Failed to analyze URL');
  }

  return await response.json();
}

