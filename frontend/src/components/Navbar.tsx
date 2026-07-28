import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Database, Activity, Sparkles, FileText, History, Upload } from 'lucide-react';

export const Navbar: React.FC = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Home', icon: Database },
    { path: '/upload', label: 'Upload CSV', icon: Upload },
    { path: '/dashboard', label: 'Dashboard', icon: Activity },
    { path: '/ai-insights', label: 'AI Insights', icon: Sparkles },
    { path: '/reports', label: 'Reports', icon: FileText },
    { path: '/history', label: 'History', icon: History },
  ];

  return (
    <header className="sticky top-0 z-50 bg-slate-900/80 backdrop-blur-md border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-3 group">
            <div className="p-2 bg-gradient-to-tr from-indigo-600 to-violet-500 rounded-xl shadow-lg shadow-indigo-500/20 group-hover:scale-105 transition-transform">
              <Database className="w-6 h-6 text-white" />
            </div>
            <div>
              <span className="font-bold text-lg text-white tracking-wide">AI Dataset</span>
              <span className="text-indigo-400 font-bold ml-1 text-lg">Copilot</span>
            </div>
          </Link>

          <nav className="flex items-center gap-1 sm:gap-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-indigo-600/20 text-indigo-400 border border-indigo-500/30'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span className="hidden md:inline">{item.label}</span>
                </Link>
              );
            })}
          </nav>
        </div>
      </div>
    </header>
  );
};
