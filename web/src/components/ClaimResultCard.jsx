import React, { useState } from 'react';

function ClaimResultCard({ claim }) {
  const [expanded, setExpanded] = useState(false);
  const [reasoningExpanded, setReasoningExpanded] = useState(false);

  const getVerdictChip = (verdict) => {
    const chips = {
      true: {
        label: '✅ True',
        color: 'bg-green-100 text-green-800 border-green-300',
      },
      false: {
        label: '❌ False',
        color: 'bg-red-100 text-red-800 border-red-300',
      },
      misleading: {
        label: '🔶 Misleading',
        color: 'bg-orange-100 text-orange-800 border-orange-300',
      },
      no_info: {
        label: '❓ No Information',
        color: 'bg-gray-100 text-gray-800 border-gray-300',
      },
    };
    const chip = chips[verdict?.toLowerCase()] || chips.no_info;
    return (
      <span className={`inline-block px-3 py-1 rounded-brand text-xs font-semibold border ${chip.color}`}>
        {chip.label}
      </span>
    );
  };

  const getConfidenceBar = (confidence) => {
    const percentage = Math.round(confidence * 100);
    const colorClass =
      percentage >= 70 ? 'bg-green-500' :
      percentage >= 40 ? 'bg-yellow-500' :
      'bg-orange-500';
    
    return (
      <div className="w-full">
        <div className="flex justify-between text-xs text-gray-600 mb-1">
          <span>Confidence</span>
          <span>{percentage}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className={`h-2 rounded-full transition-all ${colorClass}`}
            style={{ width: `${percentage}%` }}
          />
        </div>
      </div>
    );
  };

  const citations = claim.citations || claim.final_citations || [];

  return (
    <div className="bg-white border border-gray-200 rounded-brand overflow-hidden shadow-sm">
      <div className="p-6">
        {/* Claim Text */}
        <div className="mb-4">
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
            <p className={`text-xs text-gray-700 leading-relaxed ${expanded ? '' : 'line-clamp-3'}`}>
              {claim.explanation}
            </p>
            {claim.explanation.length > 200 && (
              <button
                onClick={() => setExpanded(!expanded)}
                className="text-xs text-primary hover:text-blue-600 mt-1"
              >
                {expanded ? 'Show Less' : 'Show More'}
              </button>
            )}
          </div>
        )}

        {/* Gemini Reasoning Section - Collapsible */}
        {claim.final_reasoning && (
          <div className="mb-4">
            <button
              onClick={() => setReasoningExpanded(!reasoningExpanded)}
              className="w-full text-left text-xs text-primary hover:text-blue-600 font-medium flex items-center justify-between mb-2 p-2 bg-blue-50 rounded-brand hover:bg-blue-100 transition-colors"
            >
              <span className="flex items-center gap-2">
                <span>{reasoningExpanded ? '▼' : '▶'}</span>
                <span>Gemini Reasoning</span>
              </span>
            </button>
            {reasoningExpanded && (
              <div className="p-3 bg-gray-50 rounded-brand text-xs text-gray-700 leading-relaxed">
                {claim.final_reasoning}
              </div>
            )}
          </div>
        )}

        {/* Citations */}
        {citations.length > 0 && (
          <div className="mt-4 pt-4 border-t border-gray-200">
            <h4 className="text-xs font-semibold text-gray-700 mb-2">Supporting Sources:</h4>
            <ul className="space-y-2">
              {citations.slice(0, 5).map((citation, idx) => (
                <li key={idx}>
                  <a
                    href={citation.url || citation}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-xs text-primary hover:text-blue-600 hover:underline break-all flex items-start gap-2"
                  >
                    <svg className="w-3 h-3 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                    <span>{citation.title || citation.url || citation}</span>
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default ClaimResultCard;

