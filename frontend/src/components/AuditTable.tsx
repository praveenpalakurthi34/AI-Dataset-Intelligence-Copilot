import React from 'react';
import type { ColumnSummary } from '../types';

interface AuditTableProps {
  columns: ColumnSummary[];
}

export const AuditTable: React.FC<AuditTableProps> = ({ columns }) => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
      <div className="px-6 py-4 border-b border-slate-800 flex justify-between items-center">
        <h3 className="font-bold text-white text-lg">Column Audit Details</h3>
        <span className="text-xs text-slate-400 font-mono">{columns.length} columns inspected</span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm text-slate-300">
          <thead className="bg-slate-950 text-slate-400 uppercase text-xs font-semibold tracking-wider border-b border-slate-800">
            <tr>
              <th className="px-6 py-3.5">Column Name</th>
              <th className="px-6 py-3.5">Data Type</th>
              <th className="px-6 py-3.5">Missing Values</th>
              <th className="px-6 py-3.5">Outliers</th>
              <th className="px-6 py-3.5">Unique Values</th>
              <th className="px-6 py-3.5">Stats (Min / Max)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 font-mono">
            {columns.map((col) => {
              const hasMissing = col.missing_count > 0;
              const hasOutliers = col.outlier_count > 0;
              const minVal = col.min_value;
              const maxVal = col.max_value;

              return (
                <tr key={col.column_name} className="hover:bg-slate-800/40 transition-colors">
                  <td className="px-6 py-4 font-semibold text-white">{col.column_name}</td>
                  <td className="px-6 py-4">
                    <span className="bg-slate-800 text-indigo-300 px-2.5 py-1 rounded text-xs">
                      {col.data_type}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    {hasMissing ? (
                      <span className="text-amber-400 font-medium">
                        {col.missing_count} ({col.missing_pct}%)
                      </span>
                    ) : (
                      <span className="text-emerald-400">0 (0%)</span>
                    )}
                  </td>
                  <td className="px-6 py-4">
                    {hasOutliers ? (
                      <span className="text-rose-400 font-medium">{col.outlier_count}</span>
                    ) : (
                      <span className="text-slate-500">0</span>
                    )}
                  </td>
                  <td className="px-6 py-4 text-slate-300">{col.unique_count}</td>
                  <td className="px-6 py-4 text-slate-400 text-xs">
                    {minVal != null && maxVal != null ? (
                      <span>
                        [{minVal.toFixed(1)}, {maxVal.toFixed(1)}]
                      </span>
                    ) : (
                      <span className="text-slate-600">N/A</span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
