import React, { useState } from 'react';

function HomeScreen({ onAnalyzeURL }) {
  const [url, setUrl] = useState('');
  const [isValidUrl, setIsValidUrl] = useState(false);

  const validateURL = (input) => {
    try {
      new URL(input);
      return true;
    } catch {
      return false;
    }
  };

  const handleUrlChange = (e) => {
    const value = e.target.value;
    setUrl(value);
    setIsValidUrl(validateURL(value));
  };

  const handleAnalyze = () => {
    if (isValidUrl && url.trim()) {
      onAnalyzeURL(url.trim());
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="text-center py-8 px-4">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">SIFT</h1>
        <p className="text-sm text-gray-600 mb-6">Source • Investigate • Find • Trace</p>
        
        {/* Logo Placeholder */}
        <div className="flex justify-center mb-8">
          <div className="w-24 h-24 rounded-full bg-gradient-to-br from-purple-500 to-blue-600 flex items-center justify-center shadow-lg">
            <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>
      </div>

      {/* Instructions */}
      <div className="px-6 mb-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-3">How to use SIFT</h2>
        <ul className="space-y-2 text-sm text-gray-600">
          <li className="flex items-start">
            <span className="text-purple-600 mr-2">•</span>
            <span>Highlight any text → Right click → "Analyze with SIFT"</span>
          </li>
          <li className="flex items-start">
            <span className="text-purple-600 mr-2">•</span>
            <span>Or paste a link below to analyze article credibility</span>
          </li>
          <li className="flex items-start">
            <span className="text-purple-600 mr-2">•</span>
            <span>Results include verdict, confidence & citations</span>
          </li>
        </ul>
      </div>

      {/* Divider */}
      <div className="px-6 mb-6">
        <div className="border-t border-gray-200"></div>
      </div>

      {/* URL Input */}
      <div className="px-6 mb-6">
        <input
          type="url"
          value={url}
          onChange={handleUrlChange}
          placeholder="Paste a full article URL to analyze"
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 text-sm"
        />
      </div>

      {/* Analyze Button */}
      <div className="px-6 mb-6">
        <button
          onClick={handleAnalyze}
          disabled={!isValidUrl}
          className="w-full py-3 px-4 text-white font-medium rounded-lg hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          style={{ backgroundColor: '#6A35FF' }}
        >
          Analyze
        </button>
      </div>

      {/* Footer */}
      <div className="mt-auto px-6 pb-6">
        <p className="text-xs text-gray-500 text-center">
          Privacy first • Data never stored
        </p>
      </div>
    </div>
  );
}

export default HomeScreen;
