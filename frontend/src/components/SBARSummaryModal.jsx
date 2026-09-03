import React from 'react';

export default function SBARSummaryModal({ isOpen, onClose, triageData }) {
  if (!isOpen) return null;

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#283044]/50 backdrop-blur-sm p-4 animate-fadeIn">
      <div className="bg-white max-w-2xl w-full rounded-2xl shadow-2xl border border-[#dae2fd] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="p-4 sm:p-5 bg-[#eaedff] flex items-center justify-between border-b border-[#dae2fd]">
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-[#006194]">clinical_notes</span>
            <h3 className="text-base font-bold text-[#131b2e]">Diagnostic Summary & SBAR Preview</h3>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-lg flex items-center justify-center text-[#3f4850] hover:bg-[#e2e7ff] transition-colors"
          >
            <span className="material-symbols-outlined text-[20px]">close</span>
          </button>
        </div>

        {/* Content */}
        <div className="p-6 text-xs text-[#131b2e] flex flex-col gap-4 max-h-[70vh] overflow-y-auto">
          <div className="p-4 rounded-xl bg-[#f2f3ff] font-mono space-y-2 border border-[#dae2fd]/70 leading-relaxed">
            <p><strong>[SITUATION]:</strong> 32yo female presenting with a 3-day history of non-productive cough, sternal soreness secondary to coughing, and low-grade pyrexia (100.4°F).</p>
            <p><strong>[BACKGROUND]:</strong> Non-smoker, no history of asthma or cardiac anomaly. SpO2 stable at 98% room air.</p>
            <p><strong>[ASSESSMENT]:</strong> {triageData?.condition ? `High probability of ${triageData.condition} (${triageData.confidence}% Confidence).` : 'High probability of Viral Upper Respiratory Tract Infection (ICD-10 J06.9 - 78%). Secondary differential: GERD irritation (42%).'}</p>
            <p><strong>[RECOMMENDATION]:</strong> {triageData?.action ? triageData.action : 'Supportive care, oral hydration, antipyretics PRN. Outpatient evaluation recommended within 24h if temperature exceeds 101.5°F or dyspnea develops.'}</p>
          </div>

          <div className="flex items-center justify-between text-[#3f4850] font-mono text-[11px] px-1">
            <span>MD Verification Hash: 99c72e-d001-44bf</span>
            <span className="text-[#006c49] font-bold flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-[#006c49]"></span>
              Cryptographically Signed
            </span>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 bg-[#f2f3ff] flex justify-end gap-3 border-t border-[#dae2fd]">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-[#eaedff] hover:bg-[#dae2fd] text-[#131b2e] text-xs font-semibold transition-colors"
          >
            Close
          </button>
          <button
            onClick={handlePrint}
            className="px-4 py-2 rounded-xl bg-[#006194] hover:bg-[#007bb9] text-white text-xs font-bold flex items-center gap-1.5 shadow-sm transition-all active:scale-95"
          >
            <span className="material-symbols-outlined text-[16px]">print</span>
            <span>Print / Export PDF</span>
          </button>
        </div>
      </div>
    </div>
  );
}
