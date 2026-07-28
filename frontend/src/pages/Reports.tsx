import React from 'react';
import { FileText, Download } from 'lucide-react';
import { api } from '../services/api';

export const Reports: React.FC = () => {
  const datasetId = localStorage.getItem('current_dataset_id');

  const handleDownloadPdf = () => {
    if (datasetId) {
      const downloadUrl = api.getPdfReportDownloadUrl(datasetId);
      window.open(downloadUrl, '_blank');
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-8 space-y-8">
      <div className="border-b border-slate-800 pb-4">
        <h1 className="text-3xl font-extrabold text-white">Dataset Audit PDF Reports</h1>
        <p className="text-slate-400 text-sm mt-1">Export professional PDF summary reports for stakeholders & data teams</p>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-xl flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="space-y-3">
          <div className="p-3 bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 rounded-xl w-fit">
            <FileText className="w-8 h-8" />
          </div>
          <h3 className="text-xl font-bold text-white">Export Dataset Audit PDF</h3>
          <p className="text-sm text-slate-400 max-w-md">
            Includes executive dataset summary, readiness score breakdown, quality issue list, AI recommendations, and Python cleaning code.
          </p>
        </div>

        <button
          onClick={handleDownloadPdf}
          disabled={!datasetId}
          className={`px-8 py-4 rounded-xl font-bold flex items-center gap-3 shadow-lg transition-all ${
            datasetId
              ? 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-indigo-500/25 hover:scale-105'
              : 'bg-slate-800 text-slate-500 cursor-not-allowed'
          }`}
        >
          <Download className="w-5 h-5" />
          <span>Download PDF Report</span>
        </button>
      </div>
    </div>
  );
};
