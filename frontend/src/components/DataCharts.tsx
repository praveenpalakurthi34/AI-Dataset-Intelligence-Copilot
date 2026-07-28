import React from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import type { ColumnSummary } from '../types';

interface DataChartsProps {
  columns: ColumnSummary[];
}

export const DataCharts: React.FC<DataChartsProps> = ({ columns }) => {
  const missingData = columns
    .filter((col) => col.missing_count > 0)
    .map((col) => ({
      name: col.column_name,
      missing: col.missing_count,
      pct: col.missing_pct,
    }));

  const outlierData = columns
    .filter((col) => col.outlier_count > 0)
    .map((col) => ({
      name: col.column_name,
      outliers: col.outlier_count,
    }));

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Missing Values Chart */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl">
        <h3 className="font-bold text-white text-lg mb-4">Missing Data Distribution</h3>
        {missingData.length > 0 ? (
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={missingData} margin={{ top: 10, right: 20, left: 0, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="name" stroke="#94a3b8" tick={{ fontSize: 12 }} />
                <YAxis stroke="#94a3b8" tick={{ fontSize: 12 }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff' }}
                />
                <Bar dataKey="missing" fill="#818cf8" radius={[4, 4, 0, 0]} name="Missing Count" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <div className="h-64 flex items-center justify-center text-slate-500 text-sm">
            🎉 No missing values detected in dataset columns!
          </div>
        )}
      </div>

      {/* Outlier Chart */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl">
        <h3 className="font-bold text-white text-lg mb-4">Statistical Outliers per Column</h3>
        {outlierData.length > 0 ? (
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={outlierData} margin={{ top: 10, right: 20, left: 0, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="name" stroke="#94a3b8" tick={{ fontSize: 12 }} />
                <YAxis stroke="#94a3b8" tick={{ fontSize: 12 }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff' }}
                />
                <Bar dataKey="outliers" fill="#f43f5e" radius={[4, 4, 0, 0]} name="Outliers Count" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <div className="h-64 flex items-center justify-center text-slate-500 text-sm">
            ✨ No statistical outliers detected in numeric columns!
          </div>
        )}
      </div>
    </div>
  );
};
