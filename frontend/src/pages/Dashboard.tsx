import React, { useEffect, useState } from 'react';
import { useLocation, Link } from 'react-router-dom';
import type { AuditReport } from '../types';
import { api } from '../services/api';
import { ReadinessGauge } from '../components/ReadinessGauge';
import { MetricCard } from '../components/MetricCard';
import { IssueCard } from '../components/IssueCard';
import { AuditTable } from '../components/AuditTable';
import { DataCharts } from '../components/DataCharts';
import { Database, Sparkles, Layers, AlertCircle, CopyCheck, Flame, Loader2 } from 'lucide-react';

export const Dashboard: React.FC = () => {
  const location = useLocation();
  const [report, setReport] = useState<AuditReport | null>(location.state?.report || null);
  const [loading, setLoading] = useState(!report);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!report) {
      const datasetId = localStorage.getItem('current_dataset_id');
      if (datasetId) {
        api.getAuditReport(datasetId)
          .then(data => {
            setReport(data);
            setLoading(false);
          })
          .catch(err => {
            console.error(err);
            setError('No dataset audit report found. Please upload a dataset first.');
            setLoading(false);
          });
      } else {
        setError('No dataset loaded. Please upload a CSV dataset to view the audit dashboard.');
        setLoading(false);
      }
    }
  }, [report]);

  if (loading) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center space-y-4">
        <Loader2 className="w-10 h-10 text-indigo-500 animate-spin" />
        <p className="text-slate-400 text-sm font-medium">Fetching dataset audit report...</p>
      </div>
    );
  }

  if (error || !report) {
    return (
      <div className="max-w-2xl mx-auto py-16 text-center space-y-6">
        <div className="p-4 bg-slate-900 border border-slate-800 rounded-full w-fit mx-auto text-amber-400">
          <AlertCircle className="w-8 h-8" />
        </div>
        <h2 className="text-2xl font-bold text-white">No Dataset Loaded</h2>
        <p className="text-slate-400">{error || 'Please upload a CSV dataset to view audit analysis.'}</p>
        <Link
          to="/upload"
          className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold transition-all"
        >
          <span>Upload Dataset</span>
        </Link>
      </div>
    );
  }

  const { summary, readiness_score, issues } = report;

  return (
    <div className="space-y-8 py-6">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white">Dataset Audit Dashboard</h1>
          <p className="text-slate-400 text-sm mt-1">
            Inspected <span className="text-indigo-400 font-mono font-semibold">{report.filename}</span> • {summary.total_rows.toLocaleString()} rows × {summary.total_columns} columns
          </p>
        </div>

        <Link
          to="/ai-insights"
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white font-semibold text-sm shadow-lg shadow-indigo-500/20 transition-all hover:scale-105"
        >
          <Sparkles className="w-4 h-4" />
          <span>Generate AI Reasoning & Cleaning Code</span>
        </Link>
      </div>

      {/* Readiness Gauge */}
      <ReadinessGauge score={readiness_score} />

      {/* Metrics Row */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <MetricCard title="Total Rows" value={summary.total_rows.toLocaleString()} icon={Database} color="indigo" />
        <MetricCard title="Total Columns" value={summary.total_columns} icon={Layers} color="violet" />
        <MetricCard title="Missing Cells" value={`${summary.total_missing_cells} (${summary.total_missing_pct}%)`} icon={AlertCircle} color="amber" />
        <MetricCard title="Duplicate Rows" value={`${summary.total_duplicate_rows} (${summary.total_duplicate_pct}%)`} icon={CopyCheck} color="teal" />
        <MetricCard title="Outliers (IQR)" value={summary.total_outliers} icon={Flame} color="rose" />
      </div>

      {/* Data Visual Charts */}
      <DataCharts columns={summary.column_summaries} />

      {/* Quality Issues List */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-bold text-white">Detected Quality Issues</h3>
          <span className="text-xs bg-slate-800 text-slate-300 px-3 py-1 rounded-full font-mono">
            {issues.length} Issues Found
          </span>
        </div>

        {issues.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {issues.map((issue, idx) => (
              <IssueCard key={idx} issue={issue} />
            ))}
          </div>
        ) : (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center text-slate-400">
            🎉 Outstanding! No quality issues detected in this dataset.
          </div>
        )}
      </div>

      {/* Column Details Table */}
      <AuditTable columns={summary.column_summaries} />
    </div>
  );
};
