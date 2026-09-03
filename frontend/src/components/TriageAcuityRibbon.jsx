import React from 'react';

export default function TriageAcuityRibbon({ triageData, onUnlockReport, onTriggerER }) {
  const isHighRisk = triageData?.severity?.includes('Emergency') || triageData?.severity?.includes('High Alert');
  
  return (
    <section className="w-full max-w-[1560px] mx-auto px-4 sm:px-8 pt-4 pb-3">
      <div className="w-full rounded-2xl bg-white shadow-sm border border-[#dae2fd] p-5 sm:p-6 flex flex-col xl:flex-row items-start xl:items-center justify-between gap-5 relative overflow-hidden">
        {/* Ambient Visual Indicator Accent */}
        <div className={`absolute left-0 top-0 bottom-0 w-3 rounded-l-2xl ${
          isHighRisk ? 'bg-rose-600' : 'bg-amber-500'
        }`} />

        <div className="flex items-start gap-5 pl-2 sm:pl-3">
          <div className={`w-14 h-14 rounded-2xl flex items-center justify-center shrink-0 shadow-sm ${
            isHighRisk ? 'bg-rose-50 text-rose-600' : 'bg-amber-50 text-amber-600'
          }`}>
            <span className="material-symbols-outlined text-[32px]" style={{ fontVariationSettings: "'FILL' 1" }}>
              {isHighRisk ? 'emergency' : 'warning'}
            </span>
          </div>

          <div className="flex flex-col">
            <div className="flex items-center gap-3 flex-wrap">
              <span className={`px-3 py-1 rounded-full text-xs font-extrabold tracking-wider uppercase ${
                isHighRisk 
                  ? 'bg-rose-100 text-rose-900 border border-rose-200'
                  : 'bg-amber-100 text-amber-900 border border-amber-200'
              }`}>
                {triageData?.severity ? triageData.severity : 'Triage Acuity Level 3 (Moderate)'}
              </span>

              <span className="text-xs sm:text-sm text-[#3f4850] flex items-center gap-1.5 font-medium font-mono">
                <span className="material-symbols-outlined text-[16px]">schedule</span>
                Recommended Action: {isHighRisk ? 'Immediate / Emergency Protocol' : 'Within 12–24 Hours'}
              </span>

              <span className="px-2.5 py-1 rounded bg-[#eaedff] text-xs font-mono text-[#00628d] font-bold">
                ICD-10 Protocol: {isHighRisk ? 'I20.9 / R07.9' : 'R05.9 / R50.9'}
              </span>
            </div>

            <h1 className="text-xl sm:text-2xl font-bold text-[#131b2e] mt-1.5 tracking-tight">
              {triageData?.condition 
                ? `Clinical Guidance: ${triageData.condition}`
                : 'Schedule Telehealth or Outpatient Urgent Care Evaluation'}
            </h1>

            <p className="text-sm text-[#3f4850] max-w-4xl mt-1 leading-relaxed">
              {triageData?.action 
                ? triageData.action 
                : 'Vital indicators suggest sub-acute upper respiratory infection with mild inflammatory response. Patient is hemodynamically stable. No stridor, cyanosis, or acute respiratory distress noted in self-reported telemetry.'}
            </p>
          </div>
        </div>

        {/* Quick Triage Actions */}
        <div className="flex items-center gap-3 self-end xl:self-center shrink-0 w-full xl:w-auto justify-end pt-2 xl:pt-0">
          <button
            onClick={onUnlockReport}
            type="button"
            className="px-5 py-2.5 rounded-xl bg-[#e2e7ff] hover:bg-[#dae2fd] text-[#006194] text-sm font-bold transition-all shadow-sm flex items-center gap-2 active:scale-95"
          >
            <span className="material-symbols-outlined text-[20px]">verified_user</span>
            <span>Unlock Clinical EHR Report</span>
          </button>

          <button
            onClick={onTriggerER}
            type="button"
            className="px-5 py-2.5 rounded-xl bg-[#ba1a1a] hover:bg-[#ba1a1a]/90 text-white text-sm font-bold transition-all shadow-md shadow-rose-600/20 flex items-center gap-2 active:scale-95"
          >
            <span className="material-symbols-outlined text-[20px]" style={{ fontVariationSettings: "'FILL' 1" }}>
              emergency
            </span>
            <span>Trigger ER / 911 Protocol</span>
          </button>
        </div>
      </div>
    </section>
  );
}
