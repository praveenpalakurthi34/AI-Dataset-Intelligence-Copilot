import React from 'react';
import type { ReadinessScore } from '../types';
import { ShieldCheck } from 'lucide-react';

interface ReadinessGaugeProps {
  score: ReadinessScore;
}

export const ReadinessGauge: React.FC<ReadinessGaugeProps> = ({ score }) => {
  const { overall_score, grade, status, breakdown } = score;

  const getScoreColor = (val: number) => {
    if (val >= 85) return 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10';
    if (val >= 70) return 'text-amber-400 border-amber-500/30 bg-amber-500/10';
    if (val >= 50) return 'text-orange-400 border-orange-500/30 bg-orange-500/10';
    return 'text-rose-400 border-rose-500/30 bg-rose-500/10';
  };

  const getGaugeGradient = (val: number) => {
    if (val >= 85) return '#10b981'; // emerald
    if (val >= 70) return '#f59e0b'; // amber
    if (val >= 50) return '#f97316'; // orange
    return '#f43f5e'; // rose
  };

  const strokeDashoffset = 440 - (440 * overall_score) / 100;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl relative overflow-hidden">
      <div className="absolute top-0 right-0 p-8 opacity-5">
        <ShieldCheck className="w-48 h-48 text-indigo-400" />
      </div>

      <div className="flex flex-col md:flex-row items-center justify-between gap-8 relative z-10">
        {/* Gauge Circle */}
        <div className="relative flex items-center justify-center">
          <svg className="w-44 h-44 transform -rotate-90">
            <circle
              cx="88"
              cy="88"
              r="70"
              stroke="currentColor"
              strokeWidth="12"
              className="text-slate-800"
              fill="transparent"
            />
            <circle
              cx="88"
              cy="88"
              r="70"
              stroke={getGaugeGradient(overall_score)}
              strokeWidth="12"
              strokeDasharray="440"
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              fill="transparent"
              className="transition-all duration-1000 ease-out"
            />
          </svg>
          <div className="absolute flex flex-col items-center justify-center text-center">
            <span className="text-4xl font-extrabold text-white tracking-tight">{overall_score}</span>
            <span className="text-xs uppercase font-semibold text-slate-400 tracking-wider">Out of 100</span>
          </div>
        </div>

        {/* Score Info & Grade */}
        <div className="flex-1 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-xl font-bold text-white">Dataset Readiness Score</h3>
                <span className={`px-3 py-1 text-xs font-bold rounded-full border ${getScoreColor(overall_score)}`}>
                  Grade {grade}
                </span>
              </div>
              <p className="text-sm text-slate-400 mt-1">{status}</p>
            </div>
          </div>

          {/* Breakdown Sub-bars */}
          <div className="grid grid-cols-2 gap-3 pt-2">
            <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800">
              <div className="flex justify-between text-xs font-medium text-slate-400 mb-1">
                <span>Completeness</span>
                <span className="text-slate-200">{breakdown.completeness_score}%</span>
              </div>
              <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                <div className="bg-indigo-500 h-full rounded-full" style={{ width: `${breakdown.completeness_score}%` }}></div>
              </div>
            </div>

            <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800">
              <div className="flex justify-between text-xs font-medium text-slate-400 mb-1">
                <span>Uniqueness</span>
                <span className="text-slate-200">{breakdown.uniqueness_score}%</span>
              </div>
              <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                <div className="bg-violet-500 h-full rounded-full" style={{ width: `${breakdown.uniqueness_score}%` }}></div>
              </div>
            </div>

            <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800">
              <div className="flex justify-between text-xs font-medium text-slate-400 mb-1">
                <span>Type Validity</span>
                <span className="text-slate-200">{breakdown.type_validity_score}%</span>
              </div>
              <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                <div className="bg-teal-500 h-full rounded-full" style={{ width: `${breakdown.type_validity_score}%` }}></div>
              </div>
            </div>

            <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800">
              <div className="flex justify-between text-xs font-medium text-slate-400 mb-1">
                <span>Outlier Health</span>
                <span className="text-slate-200">{breakdown.outlier_score}%</span>
              </div>
              <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                <div className="bg-amber-500 h-full rounded-full" style={{ width: `${breakdown.outlier_score}%` }}></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
