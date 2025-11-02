import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ResultsPage from './pages/ResultsPage';
import ExtensionPage from './pages/ExtensionPage';

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/result/:id" element={<ResultsPage />} />
      <Route path="/extension" element={<ExtensionPage />} />
    </Routes>
  );
}

export default App;

