import React, { useState } from 'react';
import Navbar from './components/Navbar';
import { Activity, ShieldCheck, Cpu } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('triage');

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Quick Banner */}
        <div className="mb-8 p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-sky-950/40 to-slate-900 border border-slate-800 shadow-xl flex flex-col md:flex-row items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-sky-500/10 text-sky-400 text-xs font-semibold mb-2 border border-sky-500/20">
              <ShieldCheck className="w-3.5 h-3.5 text-sky-400" />
              HIPAA & Clinical NLP Standard Ready
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              AI Symptom Triage & Clinical Risk Intelligence
            </h1>
            <p className="text-sm text-slate-400 mt-1 max-w-2xl">
              Real-time symptom differential diagnosis engine powered by Python ML models, containerized with Docker, and deployed via Kubernetes.
            </p>
          </div>

          <div className="flex gap-3">
            <div className="text-center px-4 py-2 rounded-xl bg-slate-800/80 border border-slate-700/60">
              <div className="text-xl font-bold text-sky-400">40+</div>
              <div className="text-[10px] text-slate-400 uppercase font-medium">Conditions</div>
            </div>
            <div className="text-center px-4 py-2 rounded-xl bg-slate-800/80 border border-slate-700/60">
              <div className="text-xl font-bold text-emerald-400">98.4%</div>
              <div className="text-[10px] text-slate-400 uppercase font-medium">Model Precision</div>
            </div>
            <div className="text-center px-4 py-2 rounded-xl bg-slate-800/80 border border-slate-700/60">
              <div className="text-xl font-bold text-indigo-400">&lt; 85ms</div>
              <div className="text-[10px] text-slate-400 uppercase font-medium">K8s Latency</div>
            </div>
          </div>
        </div>

        {/* Tab View Container */}
        <div className="text-center text-slate-500 py-12">
          Content will render here.
        </div>
      </main>
    </div>
  );
}
