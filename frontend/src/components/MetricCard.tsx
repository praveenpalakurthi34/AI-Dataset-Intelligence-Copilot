import React from 'react';
import type { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  color?: 'indigo' | 'amber' | 'rose' | 'teal' | 'violet';
}

export const MetricCard: React.FC<MetricCardProps> = ({ title, value, subtitle, icon: Icon, color = 'indigo' }) => {
  const colorStyles = {
    indigo: 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20',
    amber: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
    rose: 'bg-rose-500/10 text-rose-400 border-rose-500/20',
    teal: 'bg-teal-500/10 text-teal-400 border-teal-500/20',
    violet: 'bg-violet-500/10 text-violet-400 border-violet-500/20',
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 hover:border-slate-700 transition-colors">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-slate-400">{title}</span>
        <div className={`p-2.5 rounded-lg border ${colorStyles[color]}`}>
          <Icon className="w-5 h-5" />
        </div>
      </div>
      <div className="mt-3">
        <span className="text-2xl font-bold text-white tracking-tight">{value}</span>
        {subtitle && <p className="text-xs text-slate-400 mt-1">{subtitle}</p>}
      </div>
    </div>
  );
};
