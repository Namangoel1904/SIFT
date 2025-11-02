import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ClaimResultCard from '../components/ClaimResultCard';
import CircularProgress from '../components/CircularProgress';

function ResultsPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load result from sessionStorage
    const stored = sessionStorage.getItem(`analysis_${id}`);
    if (stored) {
      setResult(JSON.parse(stored));
      setLoading(false);
    } else {
      // If no stored result, redirect to home
      navigate('/');
    }
  }, [id, navigate]);

  if (loading) {
    return (
      <div className="min-h-screen bg-neutral flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin h-12 w-12 border-4 border-primary border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-gray-600">Loading results...</p>
        </div>
      </div>
    );
  }

  if (!result) {
    return null;
  }

  // Get overall final score and verdict
  const overallScore = result.final_score || result.claims?.[0]?.final_score || 50;
  const overallVerdict = result.final_verdict || result.claims?.[0]?.final_verdict || 'UNCERTAIN';

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <button
            onClick={() => navigate('/')}
            className="flex items-center text-primary hover:text-blue-600 transition-colors"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Home
          </button>
          <h1 className="text-xl font-bold text-primary">SIFT</h1>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Final Verdict Section */}
        <div className="bg-white rounded-brand shadow-lg p-8 mb-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">AI-Verified Final Score</h2>
          <div className="flex flex-col md:flex-row items-center gap-8">
            <CircularProgress score={overallScore} verdict={overallVerdict} />
            <div className="flex-1">
              {result.summary && (
                <div className="mb-4">
                  <h3 className="text-lg font-semibold text-gray-800 mb-2">Summary</h3>
                  <p className="text-gray-700">{result.summary}</p>
                </div>
              )}
              {result.final_reasoning && (
                <details className="cursor-pointer">
                  <summary className="text-sm font-semibold text-gray-600 mb-2">
                    View Full Reasoning
                  </summary>
                  <p className="text-sm text-gray-700 mt-2">{result.final_reasoning}</p>
                </details>
              )}
            </div>
          </div>
        </div>

        {/* Visual Separator */}
        <div className="border-t border-gray-300 pt-6 mb-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Claim-Level Evidence</h2>
        </div>

        {/* Claims Results */}
        {result.claims && result.claims.length > 0 ? (
          <div className="space-y-4">
            {result.claims.map((claim, index) => (
              <ClaimResultCard key={index} claim={claim} />
            ))}
          </div>
        ) : (
          <div className="bg-yellow-50 border border-yellow-200 rounded-brand p-6 text-center">
            <p className="text-yellow-800">
              Not enough reliable information found to support this claim.
            </p>
          </div>
        )}

        {/* Methodology & Limitations */}
        {(result.methodology || result.limitations) && (
          <div className="mt-8 space-y-4">
            {result.methodology && (
              <details className="bg-gray-50 border border-gray-200 rounded-brand p-4">
                <summary className="text-sm font-semibold text-gray-800 cursor-pointer">
                  Methodology
                </summary>
                <p className="text-xs text-gray-700 leading-relaxed mt-2">
                  {result.methodology}
                </p>
              </details>
            )}

            {result.limitations && (
              <details className="bg-orange-50 border border-orange-200 rounded-brand p-4">
                <summary className="text-sm font-semibold text-orange-900 cursor-pointer">
                  Limitations
                </summary>
                <p className="text-xs text-orange-800 leading-relaxed mt-2">
                  {result.limitations}
                </p>
              </details>
            )}
          </div>
        )}

        {/* Safety Message */}
        <div className="bg-blue-50 border border-blue-200 rounded-brand p-4 mt-8 text-center">
          <p className="text-xs text-blue-800">
            ⚠️ Do not rely solely on AI for factual accuracy.
          </p>
        </div>
      </div>
    </div>
  );
}

export default ResultsPage;

