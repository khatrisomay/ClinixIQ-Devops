import React, { useState } from 'react';
import Navbar from './components/Navbar';
import TriageChat from './components/TriageChat';
import AnalyticsDashboard from './components/AnalyticsDashboard';
import PricingModal from './components/PricingModal';
import ClinicalReportModal from './components/ClinicalReportModal';
import { ShieldCheck, HeartPulse } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('triage');
  const [reportModalOpen, setReportModalOpen] = useState(false);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-sky-500 selection:text-white">
      {/* Navigation */}
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Top Hero Stats Banner */}
        <div className="mb-6 p-5 rounded-2xl bg-gradient-to-r from-slate-900 via-sky-950/40 to-slate-900 border border-slate-800 shadow-xl flex flex-col md:flex-row items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-sky-500/10 text-sky-400 text-xs font-semibold mb-1.5 border border-sky-500/20">
              <ShieldCheck className="w-3.5 h-3.5 text-sky-400" />
              HIPAA & Clinical NLP Standard Ready
            </div>
            <h1 className="text-xl sm:text-2xl font-extrabold text-white tracking-tight">
              AI Symptom Triage & Clinical Risk Intelligence
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 max-w-2xl mt-0.5">
              Natural language clinical triage powered by Python XGBoost/NLP models, containerized with Docker, and deployed via Kubernetes.
            </p>
          </div>

          <div className="flex gap-3">
            <div className="text-center px-4 py-2 rounded-xl bg-slate-800/80 border border-slate-700/60">
              <div className="text-lg font-bold text-sky-400">40+</div>
              <div className="text-[10px] text-slate-400 uppercase font-medium">Conditions</div>
            </div>
            <div className="text-center px-4 py-2 rounded-xl bg-slate-800/80 border border-slate-700/60">
              <div className="text-lg font-bold text-emerald-400">98.4%</div>
              <div className="text-[10px] text-slate-400 uppercase font-medium">Precision</div>
            </div>
            <div className="text-center px-4 py-2 rounded-xl bg-slate-800/80 border border-slate-700/60">
              <div className="text-lg font-bold text-indigo-400">&lt; 85ms</div>
              <div className="text-[10px] text-slate-400 uppercase font-medium">Latency</div>
            </div>
          </div>
        </div>

        {/* Tab Routing */}
        {activeTab === 'triage' && (
          <TriageChat onOpenReport={() => setReportModalOpen(true)} />
        )}
        {activeTab === 'analytics' && (
          <AnalyticsDashboard />
        )}
        {activeTab === 'pricing' && (
          <PricingModal onSelectPlan={(plan) => alert(`Selected plan: ${plan}. Stripe billing checkout integration will activate in Phase 5!`)} />
        )}
      </main>

      {/* Clinical Diagnostic Report Modal */}
      <ClinicalReportModal
        isOpen={reportModalOpen}
        onClose={() => setReportModalOpen(false)}
      />

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950/80 py-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <div className="flex items-center space-x-2">
            <HeartPulse className="w-4 h-4 text-sky-500" />
            <span className="text-slate-400 font-semibold">ClinixIQ DevOps Platform</span>
            <span>•</span>
            <span>Production CI/CD Edition</span>
          </div>
          <div>
            Built with React 18, Vite, Tailwind CSS, Docker & Kubernetes.
          </div>
        </div>
      </footer>
    </div>
  );
}
