import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { Landing } from './pages/Landing';
import { UploadPage } from './pages/Upload';
import { Dashboard } from './pages/Dashboard';
import { AIInsights } from './pages/AIInsights';
import { Reports } from './pages/Reports';
import { HistoryPage } from './pages/History';

export const App: React.FC = () => {
  return (
    <Router>
      <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
        <Navbar />
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/upload" element={<UploadPage />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/ai-insights" element={<AIInsights />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/history" element={<HistoryPage />} />
          </Routes>
        </main>
        <footer className="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
          <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row justify-between items-center gap-2">
            <span>AI Dataset Intelligence Copilot • MVP Architecture</span>
            <span className="text-slate-600">Built with FastAPI, Pandas, Gemini 2.5 Flash, & React</span>
          </div>
        </footer>
      </div>
    </Router>
  );
};

export default App;
