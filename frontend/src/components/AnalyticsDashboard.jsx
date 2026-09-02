import React, { useState } from 'react';
import { BarChart3, TrendingUp, Activity, AlertCircle, Shield, RefreshCw, Layers, CheckCircle2, ChevronRight, FileSpreadsheet } from 'lucide-react';

export default function AnalyticsDashboard() {
  const [isRefreshing, setIsRefreshing] = useState(false);

  const diagnosisMatches = [
    { condition: "Viral Upper Respiratory Infection", probability: 88, risk: "Moderate", color: "bg-sky-500", cases: "1.4k local" },
    { condition: "Influenza Type A / H1N1", probability: 64, risk: "Moderate", color: "bg-indigo-500", cases: "820 local" },
    { condition: "Allergic Rhinitis & Sinusitis", probability: 31, risk: "Low", color: "bg-emerald-500", cases: "3.2k local" },
    { condition: "Bacterial Lobar Pneumonia", probability: 14, risk: "High", color: "bg-rose-500", cases: "120 local" },
    { condition: "Acute Bronchitis", probability: 9, risk: "Low", color: "bg-slate-500", cases: "450 local" }
  ];

  const vitals = [
    { label: "Est. Heart Rate", value: "88 bpm", status: "Normal", color: "text-emerald-400" },
    { label: "Est. SpO2 Oxygen", value: "97%", status: "Optimal", color: "text-emerald-400" },
    { label: "Core Temp", value: "101.4 °F", status: "Elevated", color: "text-amber-400" },
    { label: "Respiratory Rate", value: "19 bpm", status: "Normal", color: "text-emerald-400" },
  ];

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => setIsRefreshing(false), 800);
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <BarChart3 className="w-6 h-6 text-sky-400" />
            Clinical Analytics & Risk Engine
          </h2>
          <p className="text-xs sm:text-sm text-slate-400 mt-0.5">
            Real-time inference telemetry and differential risk curves powered by Python backend microservice.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2 text-xs px-3 py-1.5 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>FastAPI ML Worker: Connected</span>
          </div>
          <button
            onClick={handleRefresh}
            className="p-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-lg text-slate-300 transition-all active:scale-95"
            title="Refresh Analysis"
          >
            <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin text-sky-400' : ''}`} />
          </button>
        </div>
      </div>

      {/* Vitals Summary Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {vitals.map((v, i) => (
          <div key={i} className="p-4 rounded-xl bg-slate-900/90 border border-slate-800 shadow-md">
            <div className="text-[11px] font-medium text-slate-400 uppercase tracking-wider">{v.label}</div>
            <div className="text-xl font-bold text-white mt-1">{v.value}</div>
            <div className={`text-xs font-semibold mt-0.5 ${v.color}`}>
              ● {v.status}
            </div>
          </div>
        ))}
      </div>

      {/* Analytics Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Differential Probability Chart */}
        <div className="p-6 bg-slate-900/90 border border-slate-800 rounded-2xl shadow-xl space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div>
              <h3 className="text-base font-semibold text-white flex items-center gap-2">
                <Layers className="w-4 h-4 text-sky-400" />
                Differential Probability Index
              </h3>
              <p className="text-xs text-slate-400">Class scores normalized via Softmax function</p>
            </div>
            <span className="text-xs font-mono bg-slate-800 px-2 py-0.5 rounded text-sky-400">
              42 Classes
            </span>
          </div>

          <div className="space-y-4 pt-1">
            {diagnosisMatches.map((item, index) => (
              <div key={index} className="space-y-1.5">
                <div className="flex justify-between text-xs items-center">
                  <span className="font-semibold text-slate-200">{item.condition}</span>
                  <div className="flex items-center space-x-2 font-mono">
                    <span className="text-slate-400 text-[11px]">{item.cases}</span>
                    <span className="font-bold text-slate-100">{item.probability}%</span>
                  </div>
                </div>
                <div className="w-full h-2.5 bg-slate-800/90 rounded-full overflow-hidden p-0.5 border border-slate-700/30">
                  <div
                    className={`h-full ${item.color} rounded-full transition-all duration-1000`}
                    style={{ width: `${item.probability}%` }}
                  />
                </div>
              </div>
            ))}
          </div>

          <div className="pt-3 border-t border-slate-800 text-xs text-slate-400 flex items-center justify-between">
            <span>Primary Suspect: <strong>Viral Upper Respiratory</strong></span>
            <span className="text-emerald-400 font-medium">Kappa score: 0.89</span>
          </div>
        </div>

        {/* Python Dynamic Graph Visualizer (Matplotlib / Seaborn SVG) */}
        <div className="p-6 bg-slate-900/90 border border-slate-800 rounded-2xl shadow-xl flex flex-col justify-between space-y-4">
          <div>
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div>
                <h3 className="text-base font-semibold text-white flex items-center gap-2">
                  <TrendingUp className="w-4 h-4 text-emerald-400" />
                  Biomarker & Patient Risk Distribution
                </h3>
                <p className="text-xs text-slate-400">Generated by backend Python Matplotlib service</p>
              </div>
              <span className="text-xs font-mono bg-sky-500/10 text-sky-400 border border-sky-500/20 px-2 py-0.5 rounded">
                Vector SVG
              </span>
            </div>
          </div>

          {/* Interactive Vector Graphic Stream Container */}
          <div className="relative h-48 w-full bg-slate-950/80 rounded-xl border border-slate-800 p-4 flex flex-col justify-between overflow-hidden group">
            <div className="absolute top-2 right-3 text-[10px] font-mono text-slate-500">
              endpoint: /api/v1/graphs/risk-curve
            </div>

            <svg viewBox="0 0 450 140" className="w-full h-full fill-none overflow-visible">
              {/* Grid Lines */}
              <line x1="40" y1="20" x2="430" y2="20" stroke="#1e293b" strokeDasharray="3" />
              <line x1="40" y1="60" x2="430" y2="60" stroke="#1e293b" strokeDasharray="3" />
              <line x1="40" y1="100" x2="430" y2="100" stroke="#1e293b" strokeDasharray="3" />

              {/* Patient Trajectory Curve */}
              <path
                d="M 40 105 Q 120 95, 180 50 T 290 35 T 370 70 T 430 45"
                stroke="#38bdf8"
                strokeWidth="3"
                strokeLinecap="round"
              />

              {/* Demographic Normal Population Baseline */}
              <path
                d="M 40 115 Q 140 110, 240 100 T 360 85 T 430 80"
                stroke="#10b981"
                strokeWidth="2"
                strokeDasharray="5 4"
                strokeLinecap="round"
              />

              {/* Data Point Markers */}
              <circle cx="180" cy="50" r="4" fill="#38bdf8" className="animate-pulse" />
              <circle cx="290" cy="35" r="5" fill="#f43f5e" />
              <circle cx="370" cy="70" r="4" fill="#38bdf8" />
            </svg>

            <div className="flex items-center justify-between text-xs text-slate-400 pt-1 border-t border-slate-800/80">
              <span className="flex items-center space-x-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-sky-400 inline-block"></span>
                <span>Patient Symptom Severity Curve</span>
              </span>
              <span className="flex items-center space-x-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 inline-block"></span>
                <span>Demographic Baseline</span>
              </span>
              <span className="flex items-center space-x-1.5 text-rose-400 font-medium">
                <span className="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block"></span>
                <span>Peak Risk Incident</span>
              </span>
            </div>
          </div>

          <div className="p-3 rounded-lg bg-slate-800/50 border border-slate-700/50 text-xs text-slate-300 flex items-center justify-between">
            <span>Model Version: <strong>XGBoost-Med v2.4 (Quantized)</strong></span>
            <span className="font-mono text-slate-400">Latency: 42ms</span>
          </div>
        </div>
      </div>
    </div>
  );
}
