import React from 'react';
import { X, Printer, Download, Stethoscope, AlertCircle, FileText, CheckCircle2 } from 'lucide-react';

export default function ClinicalReportModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fadeIn">
      <div className="bg-slate-900 border border-slate-800 w-full max-w-2xl rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Modal Top Bar */}
        <div className="p-4 bg-slate-800/80 border-b border-slate-700/60 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <FileText className="w-5 h-5 text-sky-400" />
            <h3 className="text-base font-bold text-white">Clinical Triage Diagnostic Summary</h3>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={handlePrint}
              className="p-1.5 text-slate-300 hover:text-white bg-slate-700/60 rounded-lg text-xs flex items-center gap-1 px-2.5"
            >
              <Printer className="w-3.5 h-3.5" />
              <span>Print / PDF</span>
            </button>
            <button
              onClick={onClose}
              className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Report Content */}
        <div className="p-6 overflow-y-auto space-y-6 text-slate-300 text-xs">
          {/* Patient / Session Meta */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-950/60 p-3.5 rounded-xl border border-slate-800">
            <div>
              <span className="text-slate-500 block text-[10px] uppercase">Session ID</span>
              <span className="font-mono text-white font-semibold">CLX-2026-8941</span>
            </div>
            <div>
              <span className="text-slate-500 block text-[10px] uppercase">Date & Time</span>
              <span className="text-white font-semibold">{new Date().toLocaleDateString()}</span>
            </div>
            <div>
              <span className="text-slate-500 block text-[10px] uppercase">Triage Level</span>
              <span className="text-amber-400 font-bold">Category II - Moderate</span>
            </div>
            <div>
              <span className="text-slate-500 block text-[10px] uppercase">Model Latency</span>
              <span className="font-mono text-emerald-400 font-semibold">48 ms (K8s Pod)</span>
            </div>
          </div>

          {/* Primary Assessment */}
          <div className="space-y-2">
            <h4 className="text-sm font-bold text-white uppercase tracking-wider text-slate-400 border-b border-slate-800 pb-1">
              Primary Diagnostic Differential
            </h4>
            <div className="p-4 bg-slate-800/60 border border-slate-700/60 rounded-xl space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-base font-bold text-white">Viral Upper Respiratory Infection</span>
                <span className="text-emerald-400 font-mono font-bold text-sm">88% Probability</span>
              </div>
              <p className="text-slate-300 leading-relaxed">
                Symptoms analyzed indicate acute viral etiology affecting the upper tracheobronchial tract. Vitals indicate mild febrile response.
              </p>
            </div>
          </div>

          {/* Reported Symptoms Extracted via NLP */}
          <div className="space-y-2">
            <h4 className="text-sm font-bold text-white uppercase tracking-wider text-slate-400 border-b border-slate-800 pb-1">
              Extracted Clinical Features (NLP Tokens)
            </h4>
            <div className="flex flex-wrap gap-2">
              {["High Fever (101.4°F)", "Dry Cough", "Fatigue", "Mild Myalgia", "Pharyngeal Erythema"].map((s, i) => (
                <span key={i} className="px-2.5 py-1 rounded-md bg-slate-800 border border-slate-700 text-slate-200">
                  {s}
                </span>
              ))}
            </div>
          </div>

          {/* Recommended Next Clinical Steps */}
          <div className="p-4 bg-sky-950/30 border border-sky-500/30 rounded-xl space-y-1.5">
            <strong className="text-sky-400 font-bold block text-sm">Physician Referral & Next Steps:</strong>
            <ul className="list-disc pl-4 space-y-1 text-slate-300">
              <li>Patient should consult primary care physician within 24–48 hours if fever persists.</li>
              <li>Recommend Rapid Antigen Test (Influenza / SARS-CoV-2) to rule out viral specificities.</li>
              <li>Advise patient to monitor for warning signs: chest pain, dyspnea, or hemoptysis.</li>
            </ul>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 bg-slate-800/80 border-t border-slate-700/60 flex items-center justify-between text-[11px] text-slate-400">
          <span>ClinixIQ v1.0 • Generated for Clinical Reference Only</span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 bg-slate-700 hover:bg-slate-600 text-white rounded-lg font-medium"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
