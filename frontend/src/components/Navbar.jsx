import React, { useState } from 'react';
import { HeartPulse, Activity, Sparkles, Menu, X, ShieldCheck, Server } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const tabs = [
    { id: 'triage', label: 'Triage Assistant' },
    { id: 'analytics', label: 'Analytics & Risk' },
    { id: 'pricing', label: 'Pro Plans' },
  ];

  return (
    <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand Logo */}
        <div 
          className="flex items-center space-x-3 cursor-pointer group"
          onClick={() => { setActiveTab('triage'); setMobileMenuOpen(false); }}
        >
          <div className="p-2 bg-gradient-to-tr from-sky-500 to-indigo-600 rounded-xl shadow-lg shadow-sky-500/25 group-hover:scale-105 transition-transform">
            <HeartPulse className="w-5 h-5 text-white animate-pulse" />
          </div>
          <div>
            <span className="text-xl font-bold tracking-tight text-white">
              Clinix<span className="text-sky-400">IQ</span>
            </span>
            <span className="ml-2 text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/20">
              DevOps v1.0
            </span>
          </div>
        </div>

        {/* Desktop Tabs */}
        <nav className="hidden md:flex space-x-1">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2 text-sm font-medium rounded-lg transition-all ${
                activeTab === tab.id
                  ? 'bg-sky-500/10 text-sky-400 border border-sky-500/30 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>

        {/* Cluster Telemetry & CTA */}
        <div className="hidden lg:flex items-center space-x-4">
          <div className="flex items-center space-x-2 text-xs text-slate-400 bg-slate-800/70 px-3 py-1.5 rounded-full border border-slate-700/60 shadow-inner">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
            <span className="font-mono text-[11px] text-slate-300 flex items-center gap-1">
              <Server className="w-3 h-3 text-sky-400" /> K8s Cluster: Healthy
            </span>
          </div>

          <button
            onClick={() => setActiveTab('pricing')}
            className="flex items-center space-x-1.5 text-xs font-semibold px-4 py-2 rounded-lg bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white shadow-md shadow-sky-500/25 transition-all active:scale-95"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Upgrade to Pro</span>
          </button>
        </div>

        {/* Mobile Menu Button */}
        <div className="md:hidden flex items-center">
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 focus:outline-none"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-slate-800 bg-slate-900 px-4 pt-2 pb-4 space-y-2">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => {
                setActiveTab(tab.id);
                setMobileMenuOpen(false);
              }}
              className={`block w-full text-left px-3 py-2 text-sm font-medium rounded-lg ${
                activeTab === tab.id
                  ? 'bg-sky-500/20 text-sky-400'
                  : 'text-slate-300 hover:bg-slate-800'
              }`}
            >
              {tab.label}
            </button>
          ))}
          <div className="pt-2 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400 px-1">
            <span className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-400 inline-block"></span>
              K8s: Online
            </span>
            <button
              onClick={() => { setActiveTab('pricing'); setMobileMenuOpen(false); }}
              className="text-sky-400 font-medium"
            >
              Upgrade &rarr;
            </button>
          </div>
        </div>
      )}
    </header>
  );
}
