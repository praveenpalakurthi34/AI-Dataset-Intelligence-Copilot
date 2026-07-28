import React, { useEffect, useState } from 'react';
import { History as HistoryIcon, FileSpreadsheet, ArrowRight } from 'lucide-react';
import { api } from '../services/api';
import { Link } from 'react-router-dom';

export const HistoryPage: React.FC = () => {
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getHistory()
      .then(data => {
        setHistory(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="max-w-5xl mx-auto py-8 space-y-8">
      <div className="border-b border-slate-800 pb-4">
        <h1 className="text-3xl font-extrabold text-white">Dataset Audit History</h1>
        <p className="text-slate-400 text-sm mt-1">Review past dataset quality analysis records stored in SQLite history</p>
      </div>

      {loading ? (
        <div className="text-center py-12 text-slate-400">Loading audit history...</div>
      ) : history.length > 0 ? (
        <div className="space-y-4">
          {history.map((item) => (
            <div key={item.id} className="bg-slate-900 border border-slate-800 rounded-xl p-5 flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 rounded-lg">
                  <FileSpreadsheet className="w-6 h-6" />
                </div>
                <div>
                  <h4 className="font-bold text-white text-base">{item.filename}</h4>
                  <p className="text-xs text-slate-400">{item.analyzed_at} • Score: {item.readiness_score}/100</p>
                </div>
              </div>

              <Link
                to="/dashboard"
                onClick={() => localStorage.setItem('current_dataset_id', item.dataset_id)}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-semibold flex items-center gap-2"
              >
                <span>View Audit</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-12 text-center space-y-4">
          <HistoryIcon className="w-12 h-12 text-slate-600 mx-auto" />
          <h3 className="text-xl font-bold text-white">No Audit History Found</h3>
          <p className="text-slate-400 text-sm">Upload a dataset to start recording audit history.</p>
          <Link
            to="/upload"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-indigo-600 text-white font-bold text-sm"
          >
            <span>Upload CSV Dataset</span>
          </Link>
        </div>
      )}
    </div>
  );
};
