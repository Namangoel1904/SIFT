import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { analyzeText, analyzeURL } from '../hooks/useAPI';

function HomePage() {
  const [inputType, setInputType] = useState('text'); // 'text' or 'url'
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleAnalyze = async () => {
    if (!inputValue.trim()) {
      setError('Please enter text or URL to analyze');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      let result;
      if (inputType === 'text') {
        result = await analyzeText(inputValue);
      } else {
        result = await analyzeURL(inputValue);
      }

      // Store result in sessionStorage and navigate
      const resultId = Date.now().toString();
      sessionStorage.setItem(`analysis_${resultId}`, JSON.stringify(result));
      navigate(`/result/${resultId}`);
    } catch (err) {
      setError(err.message || 'An error occurred while analyzing');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-neutral flex flex-col items-center justify-center px-4 py-8">
      <div className="w-full max-w-2xl">
        {/* Logo and Title */}
        <div className="text-center mb-12">
          <img 
            src="/assets/logo.png" 
            alt="SIFT Logo" 
            className="w-32 h-32 mx-auto mb-6"
            onError={(e) => {
              // Fallback if logo doesn't exist
              e.target.style.display = 'none';
            }}
          />
          <h1 className="text-5xl font-bold text-primary mb-2">SIFT</h1>
          <p className="text-lg text-gray-600">Source • Investigate • Find • Trace</p>
        </div>

        {/* Input Options */}
        <div className="bg-white rounded-brand shadow-lg p-8 mb-6">
          {/* Tab Selection */}
          <div className="flex gap-4 mb-6 border-b border-gray-200">
            <button
              onClick={() => setInputType('text')}
              className={`pb-3 px-4 font-semibold transition-colors ${
                inputType === 'text'
                  ? 'text-primary border-b-2 border-primary'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              Text Input
            </button>
            <button
              onClick={() => setInputType('url')}
              className={`pb-3 px-4 font-semibold transition-colors ${
                inputType === 'url'
                  ? 'text-primary border-b-2 border-primary'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              URL Input
            </button>
          </div>

          {/* Input Field */}
          {inputType === 'text' ? (
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Paste or type the claim text you want to fact-check..."
              className="w-full h-40 p-4 border border-gray-300 rounded-brand resize-none focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
              disabled={loading}
            />
          ) : (
            <input
              type="url"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Enter article or news URL to analyze..."
              className="w-full p-4 border border-gray-300 rounded-brand focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
              disabled={loading}
            />
          )}

          {/* Error Message */}
          {error && (
            <div className="mt-4 p-3 bg-red-50 border border-error rounded-brand text-error text-sm">
              {error}
            </div>
          )}

          {/* Analyze Button */}
          <button
            onClick={handleAnalyze}
            disabled={loading || !inputValue.trim()}
            className="w-full mt-6 py-4 bg-primary text-white font-semibold rounded-brand hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyzing...
              </>
            ) : (
              'Analyze'
            )}
          </button>
        </div>

        {/* Extension Link */}
        <div className="text-center">
          <a
            href="/extension"
            className="text-primary hover:text-blue-600 font-medium transition-colors"
          >
            Download Browser Extension →
          </a>
        </div>
      </div>
    </div>
  );
}

export default HomePage;

