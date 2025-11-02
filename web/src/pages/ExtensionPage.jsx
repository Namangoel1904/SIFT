import React from 'react';
import { Link } from 'react-router-dom';

function ExtensionPage() {
  const handleDownload = () => {
    // Trigger download of extension zip
    window.location.href = '/sift-extension.zip';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link
            to="/"
            className="flex items-center text-primary hover:text-blue-600 transition-colors"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Home
          </Link>
          <h1 className="text-xl font-bold text-primary">SIFT Extension</h1>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <img 
            src="/assets/logo.png" 
            alt="SIFT Logo" 
            className="w-24 h-24 mx-auto mb-6"
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
          <h1 className="text-4xl font-bold text-primary mb-4">Install SIFT Browser Extension</h1>
          <p className="text-lg text-gray-600 mb-8">
            Get real-time fact-checking directly in your browser
          </p>
          <button
            onClick={handleDownload}
            className="bg-primary text-white font-semibold px-8 py-4 rounded-brand hover:bg-blue-600 transition-colors text-lg"
          >
            Download Extension
          </button>
        </div>

        {/* Features */}
        <div className="bg-white rounded-brand shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Features</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-12 h-12 bg-primary bg-opacity-10 rounded-brand flex items-center justify-center">
                <span className="text-2xl">🔍</span>
              </div>
              <div>
                <h3 className="font-semibold text-gray-800 mb-2">Real-time Fact-Checking</h3>
                <p className="text-sm text-gray-600">
                  Select any text on a webpage and get instant fact-check results
                </p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-12 h-12 bg-accent bg-opacity-10 rounded-brand flex items-center justify-center">
                <span className="text-2xl">🤖</span>
              </div>
              <div>
                <h3 className="font-semibold text-gray-800 mb-2">AI-Powered Analysis</h3>
                <p className="text-sm text-gray-600">
                  Uses advanced AI to extract claims and verify them against reliable sources
                </p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-12 h-12 bg-warning bg-opacity-10 rounded-brand flex items-center justify-center">
                <span className="text-2xl">🌐</span>
              </div>
              <div>
                <h3 className="font-semibold text-gray-800 mb-2">URL Analysis</h3>
                <p className="text-sm text-gray-600">
                  Analyze entire articles and news links for comprehensive fact-checking
                </p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-12 h-12 bg-primary bg-opacity-10 rounded-brand flex items-center justify-center">
                <span className="text-2xl">📊</span>
              </div>
              <div>
                <h3 className="font-semibold text-gray-800 mb-2">Detailed Results</h3>
                <p className="text-sm text-gray-600">
                  Get confidence scores, explanations, and citations from trusted sources
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Setup Instructions */}
        <div className="bg-white rounded-brand shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Installation Instructions</h2>
          
          {/* Chrome */}
          <div className="mb-8">
            <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
              <span className="text-2xl">🌐</span>
              Google Chrome
            </h3>
            <ol className="list-decimal list-inside space-y-3 text-gray-700">
              <li>Download the extension zip file using the button above</li>
              <li>Extract the zip file to a folder on your computer</li>
              <li>Open Chrome and navigate to <code className="bg-gray-100 px-2 py-1 rounded">chrome://extensions/</code></li>
              <li>Enable <strong>"Developer mode"</strong> toggle in the top right</li>
              <li>Click <strong>"Load unpacked"</strong></li>
              <li>Select the extracted extension folder</li>
              <li>The SIFT extension icon should now appear in your browser toolbar</li>
            </ol>
          </div>

          {/* Edge */}
          <div>
            <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
              <span className="text-2xl">🌐</span>
              Microsoft Edge
            </h3>
            <ol className="list-decimal list-inside space-y-3 text-gray-700">
              <li>Download the extension zip file using the button above</li>
              <li>Extract the zip file to a folder on your computer</li>
              <li>Open Edge and navigate to <code className="bg-gray-100 px-2 py-1 rounded">edge://extensions/</code></li>
              <li>Enable <strong>"Developer mode"</strong> toggle in the bottom left</li>
              <li>Click <strong>"Load unpacked"</strong></li>
              <li>Select the extracted extension folder</li>
              <li>The SIFT extension icon should now appear in your browser toolbar</li>
            </ol>
          </div>
        </div>

        {/* Screenshots Placeholder */}
        <div className="bg-white rounded-brand shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Screenshots</h2>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="bg-gray-100 rounded-brand p-12 text-center">
              <p className="text-gray-500">Screenshot placeholder: Extension Popup</p>
            </div>
            <div className="bg-gray-100 rounded-brand p-12 text-center">
              <p className="text-gray-500">Screenshot placeholder: Results View</p>
            </div>
          </div>
        </div>

        {/* Usage Instructions */}
        <div className="bg-white rounded-brand shadow-lg p-8 mt-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">How to Use</h2>
          <div className="space-y-4 text-gray-700">
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-8 h-8 bg-primary text-white rounded-full flex items-center justify-center font-bold">1</div>
              <div>
                <p className="font-semibold mb-1">Select Text on Any Webpage</p>
                <p className="text-sm text-gray-600">Highlight the text you want to fact-check</p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-8 h-8 bg-primary text-white rounded-full flex items-center justify-center font-bold">2</div>
              <div>
                <p className="font-semibold mb-1">Click the SIFT Button</p>
                <p className="text-sm text-gray-600">A "🔍 SIFT Check" button will appear near your selection</p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-8 h-8 bg-primary text-white rounded-full flex items-center justify-center font-bold">3</div>
              <div>
                <p className="font-semibold mb-1">View Results</p>
                <p className="text-sm text-gray-600">Fact-check results will appear in the extension sidebar</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ExtensionPage;

