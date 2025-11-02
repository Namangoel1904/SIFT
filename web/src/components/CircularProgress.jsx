import React from 'react';

function CircularProgress({ score, verdict }) {
  const radius = 60;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  const getColor = () => {
    if (score >= 90) return 'text-green-600 stroke-green-600';
    if (score >= 70) return 'text-green-500 stroke-green-500';
    if (score >= 40) return 'text-yellow-500 stroke-yellow-500';
    if (score >= 20) return 'text-warning stroke-warning';
    return 'text-error stroke-error';
  };

  const getVerdictLabel = () => {
    if (score >= 75) return '✅ Likely True';
    if (score >= 50) return '🟡 Mixed / Partially True';
    if (score >= 25) return '🔶 Likely Misleading';
    return '❌ False / Unsupported';
  };

  const colorClass = getColor();

  return (
    <div className="flex flex-col items-center">
      <div className="relative w-40 h-40">
        <svg className="transform -rotate-90 w-40 h-40">
          {/* Background circle */}
          <circle
            cx="80"
            cy="80"
            r={radius}
            stroke="currentColor"
            strokeWidth="10"
            fill="none"
            className="text-gray-200"
          />
          {/* Progress circle */}
          <circle
            cx="80"
            cy="80"
            r={radius}
            stroke="currentColor"
            strokeWidth="10"
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
            <div className={`text-4xl font-bold ${colorClass}`}>
              {score}
            </div>
          </div>
        </div>
      </div>
      {/* Verdict label */}
      <div className={`mt-4 text-lg font-semibold ${colorClass} text-center`}>
        {getVerdictLabel()}
      </div>
    </div>
  );
}

export default CircularProgress;

