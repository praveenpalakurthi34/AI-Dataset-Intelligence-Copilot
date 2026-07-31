import React, { useState } from 'react';
import { Sparkles, Code, CheckCircle2, Copy, AlertTriangle, Loader2 } from 'lucide-react';
import { api } from '../services/api';
import type { AIAnalysisResponse } from '../types';
import {
  autoFixDataset,
  downloadCleanedDataset,
} from "../services/autofix";
import DecisionCard from "../components/DecisionCard";



export const AIInsights: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [autoFixLoading, setAutoFixLoading] = useState(false);
  const [aiData, setAiData] = useState<AIAnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const handleGenerateAI = async () => {
    const datasetId = localStorage.getItem('current_dataset_id');
    if (!datasetId) {
      setError('Please upload and audit a dataset first.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const res = await api.analyzeAI(datasetId);
      setAiData(res);
      setLoading(false);
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || 'Failed to call Gemini AI Reasoning Service. Ensure GEMINI_API_KEY is set in backend/.env');
      setLoading(false);
    }
  };

  const handleAutoFix = async () => {
  const datasetId = localStorage.getItem("current_dataset_id");

  if (!datasetId) {
    setError("Please upload and analyze a dataset first.");
    return;
  }

  try {
    setAutoFixLoading(true);

    const result = await autoFixDataset(datasetId);

    downloadCleanedDataset(result.download_file);

    alert(result.message);

  } catch (err: any) {
    setError(err.message || "Auto Fix failed.");
  } finally {
    setAutoFixLoading(false);
  }
};
  const handleCopyCode = () => {
    if (aiData?.python_code) {
      navigator.clipboard.writeText(aiData.python_code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="space-y-8 py-6 max-w-6xl mx-auto">
      <div className="border-b border-slate-800 pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-violet-500/10 border border-violet-500/20 text-violet-400 text-xs font-semibold mb-2">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI Decision Engine</span>
          </div>
          <h1 className="text-3xl font-extrabold text-white">AI Insights & Preprocessing Code</h1>
        </div>

        <div className="flex gap-3">

  {/* Generate AI Button */}
  <button
    onClick={handleGenerateAI}
    disabled={loading}
    className="px-6 py-3 rounded-xl bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white font-bold text-sm shadow-lg shadow-indigo-500/20 flex items-center justify-center gap-2 transition-all hover:scale-105"
  >
    {loading ? (
      <>
        <Loader2 className="w-4 h-4 animate-spin" />
        <span>Analyzing...</span>
      </>
    ) : (
      <>
        <Sparkles className="w-4 h-4" />
        <span>{aiData ? "Regenerate Insights" : "Generate AI Reasoning"}</span>
      </>
    )}
  </button>

  {/* Auto Fix Button */}
  <button
    onClick={handleAutoFix}
    disabled={autoFixLoading}
    className="px-6 py-3 rounded-xl bg-gradient-to-r from-emerald-600 to-green-600 hover:from-emerald-500 hover:to-green-500 text-white font-bold text-sm shadow-lg flex items-center justify-center gap-2 transition-all hover:scale-105"
  >
    {autoFixLoading ? (
      <>
        <Loader2 className="w-4 h-4 animate-spin" />
        <span>Auto Fixing...</span>
      </>
    ) : (
      <>
        <CheckCircle2 className="w-4 h-4" />
        <span>Auto Fix Dataset</span>
      </>
    )}
  </button>

</div>
      </div>

      {error && (
        <div className="p-4 bg-amber-500/10 border border-amber-500/30 text-amber-300 rounded-xl text-sm flex items-center gap-3">
          <AlertTriangle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {aiData ? (
        <div className="space-y-8">
          {/* Summary & Explanation */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
            <h3 className="text-xl font-bold text-white flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-indigo-400" />
              <span>AI Executive Quality Summary</span>
            </h3>
            <p className="text-slate-300 text-base leading-relaxed">{aiData.health_summary}</p>
            <div className="p-4 bg-slate-950/80 rounded-xl border border-slate-800 text-sm text-slate-400 space-y-2">
              <span className="font-semibold text-slate-200 uppercase text-xs tracking-wider">Detailed Analysis:</span>
              <p>{aiData.explanation}</p>
            </div>
          </div>

          {/* AI Decisions */}
          <div className="space-y-4">
            <h3 className="text-xl font-bold text-white">
              AI Decisions
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {aiData?.decisions?.map((decision, index) => (
                <DecisionCard
                  key={index}
                  decision={decision}
                />
              ))}
            </div>
          </div>

          {/* Executable Python Cleaning Code */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
            <div className="px-6 py-4 border-b border-slate-800 flex justify-between items-center bg-slate-950">
              <div className="flex items-center gap-2">
                <Code className="w-5 h-5 text-teal-400" />
                <h3 className="font-bold text-white text-lg">Executable Python Cleaning Script</h3>
              </div>
              <button
                onClick={handleCopyCode}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-semibold flex items-center gap-2 transition-colors"
              >
                {copied ? <CheckCircle2 className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                <span>{copied ? 'Copied!' : 'Copy Code'}</span>
              </button>
            </div>
            <pre className="p-6 bg-slate-950 text-teal-300 font-mono text-sm overflow-x-auto leading-relaxed">
              <code>{aiData.python_code}</code>
            </pre>
          </div>
        </div>
      ) : (
        <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-12 text-center space-y-4">
          <Sparkles className="w-12 h-12 text-violet-400 mx-auto opacity-80" />
          <h3 className="text-xl font-bold text-white">Generate Intelligent AI Insights</h3>
          <p className="text-slate-400 text-sm max-w-md mx-auto">
            Click the button above to trigger Gemini 2.5 Flash reasoning on your structured audit report.
          </p>
        </div>
      )}
    </div>
  );
};
