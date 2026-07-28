import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, ShieldCheck, Code, Cpu, ArrowRight } from 'lucide-react';

export const Landing: React.FC = () => {
  return (
    <div className="space-y-16 py-8">
      {/* Hero Section */}
      <section className="text-center space-y-6 max-w-4xl mx-auto px-4">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-sm font-semibold">
          <Sparkles className="w-4 h-4" />
          <span>AI-Powered Dataset Intelligence for Builders</span>
        </div>
        <h1 className="text-4xl sm:text-6xl font-extrabold text-white tracking-tight leading-tight">
          Audit, Evaluate, & Fix Datasets in <span className="bg-gradient-to-r from-indigo-400 via-violet-400 to-teal-400 bg-clip-text text-transparent">Seconds</span>
        </h1>
        <p className="text-lg sm:text-xl text-slate-400 max-w-2xl mx-auto">
          Upload any CSV dataset. Instantly detect missing values, duplicates, outliers, and data type flaws. Get AI reasoning and executable Pandas cleaning code.
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
          <Link
            to="/upload"
            className="w-full sm:w-auto px-8 py-4 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white font-bold shadow-lg shadow-indigo-500/25 flex items-center justify-center gap-2 transition-all hover:scale-105"
          >
            <span>Analyze Dataset Now</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
          <Link
            to="/dashboard"
            className="w-full sm:w-auto px-8 py-4 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-200 font-semibold flex items-center justify-center gap-2 transition-all"
          >
            <span>View Demo Audit</span>
          </Link>
        </div>
      </section>

      {/* Feature Cards Grid */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-7xl mx-auto px-4">
        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4 hover:border-indigo-500/40 transition-colors">
          <div className="p-3 bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 rounded-xl w-fit">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold text-white">Rule-Based Audit Engine</h3>
          <p className="text-slate-400 text-sm leading-relaxed">
            Deterministic detection of missing values, exact duplicate rows, invalid data types, and IQR statistical outliers using Pandas and Scikit-Learn.
          </p>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4 hover:border-violet-500/40 transition-colors">
          <div className="p-3 bg-violet-500/10 border border-violet-500/20 text-violet-400 rounded-xl w-fit">
            <Cpu className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold text-white">Gemini AI Reasoning</h3>
          <p className="text-slate-400 text-sm leading-relaxed">
            Gemini 2.5 Flash analyzes JSON audit reports (never raw data) to explain quality anomalies and suggest high-impact remediation steps.
          </p>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4 hover:border-teal-500/40 transition-colors">
          <div className="p-3 bg-teal-500/10 border border-teal-500/20 text-teal-400 rounded-xl w-fit">
            <Code className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold text-white">Auto-Generated Cleaning Code</h3>
          <p className="text-slate-400 text-sm leading-relaxed">
            Receive self-contained, copy-pasteable Python script snippets to automate data preprocessing and dataset repair.
          </p>
        </div>
      </section>

      {/* How it works */}
      <section className="bg-slate-900/60 border border-slate-800 rounded-3xl p-8 max-w-5xl mx-auto space-y-8">
        <div className="text-center space-y-2">
          <h2 className="text-2xl font-bold text-white">Automated Quality Workflow</h2>
          <p className="text-slate-400 text-sm">Four simple steps to dataset perfection</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-4 gap-6 text-center">
          <div className="space-y-2">
            <div className="w-10 h-10 bg-indigo-600 text-white font-bold rounded-full flex items-center justify-center mx-auto shadow-lg shadow-indigo-600/30">1</div>
            <h4 className="font-semibold text-white">Upload CSV</h4>
            <p className="text-xs text-slate-400">Drag & drop dataset file</p>
          </div>

          <div className="space-y-2">
            <div className="w-10 h-10 bg-violet-600 text-white font-bold rounded-full flex items-center justify-center mx-auto shadow-lg shadow-violet-600/30">2</div>
            <h4 className="font-semibold text-white">Rule Audit</h4>
            <p className="text-xs text-slate-400">Compute Readiness Score</p>
          </div>

          <div className="space-y-2">
            <div className="w-10 h-10 bg-teal-600 text-white font-bold rounded-full flex items-center justify-center mx-auto shadow-lg shadow-teal-600/30">3</div>
            <h4 className="font-semibold text-white">AI Reasoning</h4>
            <p className="text-xs text-slate-400">Gemini generates insights</p>
          </div>

          <div className="space-y-2">
            <div className="w-10 h-10 bg-amber-600 text-white font-bold rounded-full flex items-center justify-center mx-auto shadow-lg shadow-amber-600/30">4</div>
            <h4 className="font-semibold text-white">Export & Clean</h4>
            <p className="text-xs text-slate-400">Get code & PDF report</p>
          </div>
        </div>
      </section>
    </div>
  );
};
