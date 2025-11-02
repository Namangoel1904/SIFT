import React, { useState, useEffect } from 'react';
import HomeScreen from './components/HomeScreen';
import ClaimResultCard from './components/ClaimResultCard';
import Loader from './components/Loader';
import ErrorState from './components/ErrorState';

const API_URL = 'http://localhost:8000';

function App() {
  const [mode, setMode] = useState('home'); // 'home' or 'results'
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [analyzedText, setAnalyzedText] = useState('');
  const [analyzedUrl, setAnalyzedUrl] = useState('');

  useEffect(() => {
    // Listen for analysis requests from background script
    const checkStorage = () => {
      chrome.storage.local.get(['pendingAnalysis', 'analysisResult', 'analysisError'], (data) => {
        if (data.pendingAnalysis) {
          const { text, url } = data.pendingAnalysis;
          setAnalyzedText(text || '');
          setAnalyzedUrl(url || '');
          setMode('results');
          analyzeText(text || '', url || '');
          chrome.storage.local.remove('pendingAnalysis');
        } else if (data.analysisResult) {
          setResults(data.analysisResult);
          setLoading(false);
          setMode('results');
          chrome.storage.local.remove('analysisResult');
        } else if (data.analysisError) {
          setError(data.analysisError);
          setLoading(false);
          setMode('results');
          chrome.storage.local.remove('analysisError');
        }
      });
    };

    // Check immediately
    checkStorage();

    // Set up storage listener for real-time updates
    const listener = (changes, areaName) => {
      if (areaName === 'local') {
        if (changes.pendingAnalysis?.newValue) {
          const { text, url } = changes.pendingAnalysis.newValue;
          setAnalyzedText(text || '');
          setAnalyzedUrl(url || '');
          setMode('results');
          analyzeText(text || '', url || '');
        } else if (changes.analysisResult?.newValue) {
          setResults(changes.analysisResult.newValue);
          setLoading(false);
          setMode('results');
        } else if (changes.analysisError?.newValue) {
          setError(changes.analysisError.newValue);
          setLoading(false);
          setMode('results');
        }
      }
    };

    chrome.storage.onChanged.addListener(listener);

    return () => {
      chrome.storage.onChanged.removeListener(listener);
    };
  }, []);

  const analyzeText = async (text, url = null) => {
    if (!text || text.length < 10) {
      setError('Text must be at least 10 characters long');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);
    setMode('results');

    try {
      const response = await fetch(`${API_URL}/api/v1/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text, url }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to analyze text');
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message || 'An error occurred while analyzing text');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeURL = async (url) => {
    if (!url || !isValidURL(url)) {
      setError('Please enter a valid URL');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);
    setAnalyzedUrl(url);
    setAnalyzedText('');
    setMode('results');

    try {
      const response = await fetch(`${API_URL}/api/v1/analyze/url`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to analyze URL');
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message || 'An error occurred while analyzing URL');
      console.error('URL analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const isValidURL = (string) => {
    try {
      new URL(string);
      return true;
    } catch (_) {
      return false;
    }
  };

  const handleBackToHome = () => {
    setMode('home');
    setResults(null);
    setError(null);
    setAnalyzedText('');
    setAnalyzedUrl('');
  };

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Close Button (top-right) */}
      <div className="flex justify-end p-4">
        <button
          onClick={() => {
            // Signal to close sidebar
            if (window.parent) {
              window.parent.postMessage({ action: 'closeSidebar' }, '*');
            }
          }}
          className="text-gray-400 hover:text-gray-600 transition-colors"
          aria-label="Close"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto">
        {mode === 'home' ? (
          <HomeScreen onAnalyzeURL={handleAnalyzeURL} />
        ) : (
          <div className="px-6 pb-6">
            {/* Breadcrumb */}
            <button
              onClick={handleBackToHome}
              className="flex items-center text-sm text-purple-600 hover:text-purple-700 mb-6 mt-2 transition-colors"
            >
              <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Back to Home
            </button>

            {loading && (
              <Loader message="Analyzing… Thinking critically…" />
            )}

            {error && (
              <ErrorState
                message={error}
                onRetry={() => {
                  if (analyzedText) {
                    analyzeText(analyzedText, analyzedUrl || null);
                  }
                }}
              />
            )}

            {results && !loading && (
              <div className="space-y-6">
                {/* Analyzed Text/URL Preview */}
                {(analyzedText || analyzedUrl) && (
                  <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                    <div className="text-xs font-semibold text-purple-900 mb-1">Analyzing:</div>
                    <div className="text-sm text-purple-800 line-clamp-3">
                      {analyzedText || analyzedUrl}
                    </div>
                  </div>
                )}

                {/* Summary */}
                {results.summary && results.claims && results.claims.length > 0 && (
                  <div className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm">
                    <h2 className="text-lg font-semibold text-gray-800 mb-2">Summary</h2>
                    <p className="text-sm text-gray-700">
                      Total claims evaluated: {results.claims.length}. AI uses combined evidence across all claims to determine the overall rating.
                    </p>
                  </div>
                )}

                {/* Claims Results */}
                {results.claims && results.claims.length > 0 ? (
                  <div className="space-y-4">
                    {/* Visual separator before claim-level evidence */}
                    <div className="border-t border-gray-300 pt-4">
                      <h2 className="text-lg font-semibold text-gray-800 mb-4">Claim-Level Evidence</h2>
                    </div>
                    {results.claims.map((claim, index) => (
                      <ClaimResultCard key={index} claim={claim} />
                    ))}
                  </div>
                ) : (
                  <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-center">
                    <p className="text-sm text-yellow-800">
                      Not enough reliable information found to support this claim.
                    </p>
                  </div>
                )}

                {/* Methodology & Limitations */}
                {(results.methodology || results.limitations) && (
                  <div className="space-y-4">
                    {results.methodology && (
                      <details className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                        <summary className="text-sm font-semibold text-gray-800 cursor-pointer">
                          Methodology
                        </summary>
                        <p className="text-xs text-gray-700 leading-relaxed mt-2">
                          {results.methodology}
                        </p>
                      </details>
                    )}

                    {results.limitations && (
                      <details className="bg-orange-50 border border-orange-200 rounded-lg p-4">
                        <summary className="text-sm font-semibold text-orange-900 cursor-pointer">
                          Limitations
                        </summary>
                        <p className="text-xs text-orange-800 leading-relaxed mt-2">
                          {results.limitations}
                        </p>
                      </details>
                    )}
                  </div>
                )}

                {/* Safety Message */}
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <p className="text-xs text-blue-800 text-center">
                    ⚠️ Do not rely solely on AI for factual accuracy.
                  </p>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
