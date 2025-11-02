import React, { useState, useRef } from 'react';

function ClaimResultCard({ claim }) {
  const [expanded, setExpanded] = useState(false);
  const [reasoningExpanded, setReasoningExpanded] = useState(false);
  const citationsRef = useRef(null);

  const scrollToCitations = () => {
    if (citationsRef.current) {
      citationsRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  const getFinalScoreColor = (score) => {
    if (score >= 90) return 'text-green-600 stroke-green-600';
    if (score >= 70) return 'text-green-500 stroke-green-500';
    if (score >= 40) return 'text-yellow-500 stroke-yellow-500';
    if (score >= 20) return 'text-orange-500 stroke-orange-500';
    return 'text-red-600 stroke-red-600';
  };

  const getFinalVerdictLabel = (score, verdict) => {
    // Dynamic badge text based on score ranges (UI only)
    if (score >= 75) {
      return '✅ Likely True';
    } else if (score >= 50) {
      return '🟡 Mixed / Partially True';
    } else if (score >= 25) {
      return '🔶 Likely Misleading';
    } else {
      return '❌ False / Unsupported';
    }
  };

  const getVerdictChip = (verdict) => {
    const chips = {
      true: {
        label: '✅ True',
        color: 'bg-green-100 text-green-800 border-green-300',
        icon: '✅'
      },
      false: {
        label: '❌ False',
        color: 'bg-red-100 text-red-800 border-red-300',
        icon: '❌'
      },
      misleading: {
        label: '🔶 Misleading',
        color: 'bg-orange-100 text-orange-800 border-orange-300',
        icon: '🔶'
      },
      no_info: {
        label: '⚪ No Info',
        color: 'bg-gray-100 text-gray-800 border-gray-300',
        icon: '⚪'
      }
    };

    const chip = chips[verdict] || chips.no_info;
    return (
      <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${chip.color} inline-flex items-center gap-1`}>
        <span>{chip.icon}</span>
        <span>{chip.label}</span>
      </span>
    );
  };

  const getConfidenceBar = (confidence) => {
    const percentage = Math.round(confidence * 100);
    const color = confidence >= 0.7 ? 'bg-green-500' : confidence >= 0.4 ? 'bg-yellow-500' : 'bg-red-500';
    
    return (
      <div className="w-full">
        <div className="flex justify-between items-center mb-1">
          <span className="text-xs text-gray-600">Confidence</span>
          <span className="text-xs font-medium text-gray-700">
            {percentage}%
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className={`h-2 rounded-full ${color} transition-all`}
            style={{ width: `${percentage}%` }}
          />
        </div>
      </div>
    );
  };

  // Circular progress ring component
  const CircularProgress = ({ score, verdict }) => {
    const radius = 40;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (score / 100) * circumference;
    const colorClass = getFinalScoreColor(score);

    return (
      <div className="flex flex-col items-center">
        <div className="relative w-24 h-24">
          <svg className="transform -rotate-90 w-24 h-24">
            {/* Background circle */}
            <circle
              cx="48"
              cy="48"
              r={radius}
              stroke="currentColor"
              strokeWidth="8"
              fill="none"
              className="text-gray-200"
            />
            {/* Progress circle */}
            <circle
              cx="48"
              cy="48"
              r={radius}
              stroke="currentColor"
              strokeWidth="8"
              fill="none"
              strokeDasharray={circumference}
              strokeDashoffset={offset}
              strokeLinecap="round"
              className={`${colorClass} transition-all duration-500`}
            />
          </svg>
          {/* Score text */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center">
              <div className={`text-2xl font-bold ${colorClass}`}>
                {score}
              </div>
            </div>
          </div>
        </div>
        {/* Verdict label - dynamic based on score */}
        <div className={`mt-2 text-sm font-semibold ${colorClass.replace('stroke-', 'text-')} text-center`}>
          {getFinalVerdictLabel(score, verdict)}
        </div>
      </div>
    );
  };

  const finalScore = claim.final_score !== undefined ? claim.final_score : (claim.confidence ? Math.round(claim.confidence * 100) : 50);
  const finalVerdict = claim.final_verdict || claim.verdict?.toUpperCase() || 'UNCERTAIN';

  return (
    <div className="bg-white border border-gray-200 rounded-lg overflow-hidden shadow-sm">
      <div className="p-4">
        {/* Final AI-Verified Score - Top Section */}
        {claim.final_score !== undefined && (
          <div className="mb-4 pb-4 border-b border-gray-200">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <h3 className="text-xs font-semibold text-gray-600">AI-Verified Final Score</h3>
                  {/* Tooltip icon */}
                  <div className="group relative">
                    <svg 
                      className="w-4 h-4 text-gray-400 hover:text-gray-600 cursor-help" 
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    {/* Tooltip */}
                    <div className="absolute left-1/2 transform -translate-x-1/2 bottom-full mb-2 w-64 p-2 bg-gray-800 text-white text-xs rounded shadow-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-10">
                      Overall truth scoring may differ from sub-claim ratings if some details are misleading or uncertain.
                      <div className="absolute top-full left-1/2 transform -translate-x-1/2 -mt-1">
                        <div className="w-2 h-2 bg-gray-800 transform rotate-45"></div>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <CircularProgress score={finalScore} verdict={finalVerdict} />
                  <div className="flex-1">
                    {claim.final_reasoning && (
                      <div 
                        className="text-xs text-gray-700 line-clamp-2 cursor-help"
                        title={claim.final_reasoning}
                      >
                        {claim.final_reasoning.substring(0, 150)}...
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Claim Text */}
        <div className="mb-3">
          <p className="text-sm font-medium text-gray-800 leading-relaxed">
            {claim.claim}
          </p>
          {/* Helper text for sub-claim analysis */}
          <p className="text-xs text-gray-500 italic mt-1">
            Sub-claim analysis — may not reflect entire statement.
          </p>
          {claim.claim_translated && claim.original_claim && claim.original_claim !== claim.claim && (
            <div className="mt-2 text-xs text-gray-500 italic">
              <span className="font-medium">Original:</span> {claim.original_claim.substring(0, 100)}...
            </div>
          )}
        </div>

        {/* Verdict Chip */}
        <div className="mb-3">
          {getVerdictChip(claim.verdict)}
        </div>

        {/* Confidence */}
        {claim.confidence !== undefined && (
          <div className="mb-4">
            {getConfidenceBar(claim.confidence)}
          </div>
        )}

        {/* Explanation */}
        {claim.explanation && (
          <div className="mb-4">
            <p className="text-xs text-gray-700 leading-relaxed line-clamp-3">
              {claim.explanation}
            </p>
          </div>
        )}

        {/* Gemini Reasoning Section - Collapsible */}
        {claim.final_reasoning && (
          <div className="mb-4">
            <button
              onClick={() => setReasoningExpanded(!reasoningExpanded)}
              className="w-full text-left text-xs text-purple-600 hover:text-purple-700 font-medium flex items-center justify-between mb-2 p-2 bg-purple-50 rounded hover:bg-purple-100 transition-colors"
            >
              <span className="flex items-center gap-2">
                <span>{reasoningExpanded ? '▼' : '▶'}</span>
                <span>Gemini Reasoning</span>
              </span>
              <span className="text-xs text-gray-500">({finalScore}/100)</span>
            </button>

            {reasoningExpanded && (
              <div className="mt-2 p-3 bg-purple-50 rounded border border-purple-200">
                <p className="text-xs text-gray-800 leading-relaxed whitespace-pre-wrap">
                  {claim.final_reasoning}
                </p>
                {claim.final_citations && claim.final_citations.length > 0 && (
                  <div className="mt-2 pt-2 border-t border-purple-200">
                    <p className="text-xs font-semibold text-gray-700 mb-1">Key Citations:</p>
                    <ul className="list-disc list-inside space-y-1">
                      {claim.final_citations.map((cite, idx) => (
                        <li key={idx} className="text-xs">
                          <a
                            href={cite}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-purple-700 hover:text-purple-800 hover:underline break-all"
                          >
                            {cite}
                          </a>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Citations */}
        {claim.citations && claim.citations.length > 0 && (
          <div className="mb-3" ref={citationsRef}>
            <div className="flex items-center justify-between mb-2">
              <button
                onClick={() => setExpanded(!expanded)}
                className="text-xs text-purple-600 hover:text-purple-700 font-medium flex items-center gap-1"
              >
                {expanded ? '▼' : '▶'} {claim.citations.length} Citation{claim.citations.length !== 1 ? 's' : ''}
              </button>
              {!expanded && (
                <button
                  onClick={scrollToCitations}
                  className="text-xs text-purple-600 hover:text-purple-700 font-medium"
                >
                  View Citations →
                </button>
              )}
            </div>

            {expanded && (
              <div className="mt-2 space-y-2">
                {claim.citations.map((citation, idx) => (
                  <a
                    key={idx}
                    href={citation}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block p-2 bg-gray-50 rounded border border-gray-200 hover:bg-gray-100 transition-colors break-all"
                  >
                    <div className="text-xs text-purple-700 truncate flex items-start">
                      <svg className="w-3 h-3 mt-0.5 mr-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                      </svg>
                      <span className="truncate">{citation}</span>
                    </div>
                  </a>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default ClaimResultCard;
