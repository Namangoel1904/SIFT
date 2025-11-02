import React from 'react';

function Loader({ message = "Analyzing… Thinking critically…" }) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="relative w-16 h-16 mb-4">
        <div className="absolute top-0 left-0 w-full h-full border-4 border-purple-200 rounded-full"></div>
        <div className="absolute top-0 left-0 w-full h-full border-4 border-purple-600 rounded-full border-t-transparent animate-spin" style={{ borderColor: '#6A35FF', borderTopColor: 'transparent' }}></div>
      </div>
      <p className="text-sm text-gray-600 font-medium">{message}</p>
      <p className="text-xs text-gray-400 mt-1">This may take a few moments</p>
    </div>
  );
}

export default Loader;
