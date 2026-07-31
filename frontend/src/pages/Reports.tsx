import React, { useState } from 'react';
import { FileText, Download, Wrench, Loader2 } from 'lucide-react';
import { api } from '../services/api';
import {
  autoFixDataset,
  downloadCleanedDataset,
} from '../services/autofix';

export const Reports: React.FC = () => {
  const datasetId = localStorage.getItem('current_dataset_id');

  const [autoFixLoading, setAutoFixLoading] = useState(false);

  const handleDownloadPdf = () => {
    if (datasetId) {
      const downloadUrl = api.getPdfReportDownloadUrl(datasetId);
      window.open(downloadUrl, '_blank');
    }
  };

  const handleAutoFix = async () => {
    if (!datasetId) {
      alert("Please upload and analyze a dataset first.");
      return;
    }

    try {
      setAutoFixLoading(true);

      const result = await autoFixDataset(datasetId);

      downloadCleanedDataset(result.download_file);

      alert(result.message);

    } catch (err: any) {
      alert(err.message || "Auto Fix failed.");
    } finally {
      setAutoFixLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-8 space-y-8">

      <div className="border-b border-slate-800 pb-4">
        <h1 className="text-3xl font-extrabold text-white">
          Dataset Reports
        </h1>

        <p className="text-slate-400 text-sm mt-1">
          Export audit reports or automatically clean your dataset.
        </p>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-xl flex flex-col md:flex-row items-center justify-between gap-6">

        <div className="space-y-3">

          <div className="p-3 bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 rounded-xl w-fit">
            <FileText className="w-8 h-8" />
          </div>

          <h3 className="text-xl font-bold text-white">
            Export Dataset Audit PDF
          </h3>

          <p className="text-sm text-slate-400 max-w-md">
            Download the audit report or automatically clean your dataset
            using the AI Decision Engine.
          </p>

        </div>

        <div className="flex flex-col sm:flex-row gap-4">

          <button
            onClick={handleDownloadPdf}
            disabled={!datasetId}
            className={`px-6 py-3 rounded-xl font-bold flex items-center gap-2 transition-all ${
              datasetId
                ? "bg-indigo-600 hover:bg-indigo-500 text-white"
                : "bg-slate-800 text-slate-500 cursor-not-allowed"
            }`}
          >
            <Download className="w-5 h-5" />
            Download PDF
          </button>

          <button
            onClick={handleAutoFix}
            disabled={!datasetId || autoFixLoading}
            className={`px-6 py-3 rounded-xl font-bold flex items-center gap-2 transition-all ${
              datasetId
                ? "bg-emerald-600 hover:bg-emerald-500 text-white"
                : "bg-slate-800 text-slate-500 cursor-not-allowed"
            }`}
          >
            {autoFixLoading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Auto Fixing...
              </>
            ) : (
              <>
                <Wrench className="w-5 h-5" />
                Auto Fix Dataset
              </>
            )}
          </button>

        </div>

      </div>

    </div>
  );
};