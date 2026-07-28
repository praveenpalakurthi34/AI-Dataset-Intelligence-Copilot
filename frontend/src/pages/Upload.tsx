import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload as UploadIcon, FileSpreadsheet, Loader2, CheckCircle2, AlertCircle } from 'lucide-react';
import { api } from '../services/api';

export const UploadPage: React.FC = () => {
  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string>('');
  const [error, setError] = useState<string | null>(null);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (!file.name.endsWith('.csv')) {
        setError('Please select a valid .csv file.');
        return;
      }
      setSelectedFile(file);
      setError(null);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (!file.name.endsWith('.csv')) {
        setError('Please drop a valid .csv file.');
        return;
      }
      setSelectedFile(file);
      setError(null);
    }
  };

  const handleUploadAndAnalyze = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError(null);

    try {
      // Step 1: Upload CSV
      setStatusMessage('Uploading CSV dataset...');
      const uploadRes = await api.uploadDataset(selectedFile);
      const datasetId = uploadRes.dataset_id;

      // Step 2: Analyze dataset
      setStatusMessage('Running rule-based dataset analysis engine...');
      const report = await api.analyzeDataset(datasetId);

      // Save datasetId to localStorage for dashboard retrieval
      localStorage.setItem('current_dataset_id', datasetId);

      setStatusMessage('Analysis complete! Redirecting to dashboard...');
      setTimeout(() => {
        navigate('/dashboard', { state: { report } });
      }, 500);

    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || 'Failed to process dataset. Please check backend server.');
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-12 px-4 space-y-8">
      <div className="text-center space-y-3">
        <h1 className="text-3xl font-extrabold text-white">Upload Dataset for Audit</h1>
        <p className="text-slate-400 text-sm">
          Select any CSV dataset. Max size 50MB.
        </p>
      </div>

      {/* Drag & Drop Upload Container */}
      <div
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-2xl p-10 text-center transition-all bg-slate-900/60 ${
          selectedFile ? 'border-indigo-500 bg-indigo-500/5' : 'border-slate-800 hover:border-indigo-500/50'
        }`}
      >
        <input
          type="file"
          accept=".csv"
          onChange={handleFileSelect}
          className="hidden"
          id="csv-upload-input"
        />

        <label htmlFor="csv-upload-input" className="cursor-pointer flex flex-col items-center gap-4">
          <div className="p-4 bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 rounded-full">
            <UploadIcon className="w-8 h-8" />
          </div>

          <div>
            <span className="font-bold text-lg text-white">Click to upload</span> or drag and drop CSV
            <p className="text-xs text-slate-500 mt-1">Supports standard CSV files with comma, semicolon or tab separation</p>
          </div>
        </label>

        {selectedFile && (
          <div className="mt-6 p-4 bg-slate-800/80 rounded-xl border border-slate-700 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <FileSpreadsheet className="w-6 h-6 text-indigo-400" />
              <div className="text-left">
                <p className="font-semibold text-white text-sm">{selectedFile.name}</p>
                <p className="text-xs text-slate-400">{(selectedFile.size / (1024 * 1024)).toFixed(2)} MB</p>
              </div>
            </div>
            <CheckCircle2 className="w-5 h-5 text-emerald-400" />
          </div>
        )}
      </div>

      {error && (
        <div className="p-4 bg-rose-500/10 border border-rose-500/30 text-rose-400 rounded-xl flex items-center gap-3 text-sm">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Action CTA */}
      <div className="flex flex-col items-center gap-4">
        <button
          onClick={handleUploadAndAnalyze}
          disabled={!selectedFile || loading}
          className={`w-full sm:w-auto px-10 py-4 rounded-xl font-bold shadow-lg flex items-center justify-center gap-3 transition-all ${
            !selectedFile || loading
              ? 'bg-slate-800 text-slate-500 cursor-not-allowed'
              : 'bg-gradient-to-r from-indigo-600 to-violet-600 text-white hover:from-indigo-500 hover:to-violet-500 hover:scale-105 shadow-indigo-500/25'
          }`}
        >
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>{statusMessage}</span>
            </>
          ) : (
            <>
              <UploadIcon className="w-5 h-5" />
              <span>Start Quality Audit</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
};
