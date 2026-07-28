import React from 'react';
import type { QualityIssue } from '../types';
import { AlertCircle, AlertTriangle, Info, OctagonAlert } from 'lucide-react';

interface IssueCardProps {
  issue: QualityIssue;
}

export const IssueCard: React.FC<IssueCardProps> = ({ issue }) => {
  const getSeverityBadge = (severity: string) => {
    switch (severity) {
      case 'critical':
        return {
          icon: OctagonAlert,
          bg: 'bg-rose-500/10 text-rose-400 border-rose-500/30',
          badgeText: 'CRITICAL',
        };
      case 'high':
        return {
          icon: AlertTriangle,
          bg: 'bg-orange-500/10 text-orange-400 border-orange-500/30',
          badgeText: 'HIGH',
        };
      case 'medium':
        return {
          icon: AlertCircle,
          bg: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
          badgeText: 'MEDIUM',
        };
      default:
        return {
          icon: Info,
          bg: 'bg-blue-500/10 text-blue-400 border-blue-500/30',
          badgeText: 'LOW',
        };
    }
  };

  const badge = getSeverityBadge(issue.severity);
  const Icon = badge.icon;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-slate-700 transition-colors">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3">
          <div className={`p-2 rounded-lg border mt-0.5 ${badge.bg}`}>
            <Icon className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h4 className="font-semibold text-slate-100">{issue.title}</h4>
              {issue.column && (
                <span className="text-xs bg-slate-800 text-slate-300 px-2 py-0.5 rounded font-mono">
                  {issue.column}
                </span>
              )}
            </div>
            <p className="text-sm text-slate-400 mt-1">{issue.description}</p>
          </div>
        </div>
        <span className={`px-2.5 py-1 text-xs font-bold rounded-full border ${badge.bg}`}>
          {badge.badgeText}
        </span>
      </div>
    </div>
  );
};
