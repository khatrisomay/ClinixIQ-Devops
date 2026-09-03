import React from 'react';

export default function AnalyticsPanel({ triageData, onOpenSummaryModal, onDownloadPDF }) {
  const liveDifferentials = triageData?.differentials;

  const topMatches = liveDifferentials ? [
    { rank: 1, name: liveDifferentials[0]?.condition || "Viral Upper Respiratory Infection", icd: "ICD-10: J06.9", prob: liveDifferentials[0]?.probability || 78, range: "72% – 84%", color: "bg-[#006194]", matchBadge: "High Match", badgeColor: "text-[#006c49]", support: "Supporting: Acute onset, dry hacking cough, low-grade pyrexia." },
    { rank: 2, name: liveDifferentials[1]?.condition || "Gastroesophageal Reflux (GERD)", icd: "ICD-10: K21.9", prob: liveDifferentials[1]?.probability || 42, range: "36% – 48%", color: "bg-[#00628d]", matchBadge: "Moderate Secondary Match", badgeColor: "text-[#00628d]", support: "Supporting: Nocturnal cough worsening in supine position; non-productive." },
    { rank: 3, name: liveDifferentials[2]?.condition || "Seasonal Allergic Rhinitis", icd: "ICD-10: J30.2", prob: liveDifferentials[2]?.probability || 25, range: "20% – 30%", color: "bg-[#707881]", matchBadge: "Low/Possible", badgeColor: "text-[#707881]", support: "Supporting: Pruritic throat, absence of wheezing, non-purulent drainage." },
    { rank: 4, name: liveDifferentials[3]?.condition || "Acute Bronchitis (Early Stage)", icd: "ICD-10: J20.9", prob: liveDifferentials[3]?.probability || 14, range: "10% – 18%", color: "bg-[#bfc7d2]", matchBadge: "Marginal Probability", badgeColor: "text-[#707881]", support: "Substernal tightness noted; low incidence of deep bronchial rhonchi." },
  ] : [
    { rank: 1, name: "Viral Upper Respiratory Tract Infection (URTI)", icd: "ICD-10: J06.9", prob: 78, range: "72% – 84%", color: "bg-[#006194]", matchBadge: "High Match", badgeColor: "text-[#006c49]", support: "Supporting: Acute onset, dry hacking cough, low-grade pyrexia." },
    { rank: 2, name: "Gastroesophageal Reflux (GERD) with Laryngopharyngeal Irritation", icd: "ICD-10: K21.9", prob: 42, range: "36% – 48%", color: "bg-[#00628d]", matchBadge: "Moderate Secondary Match", badgeColor: "text-[#00628d]", support: "Supporting: Nocturnal cough worsening in supine position; non-productive." },
    { rank: 3, name: "Seasonal Allergic Rhinitis with Reactive Tracheobronchitis", icd: "ICD-10: J30.2", prob: 25, range: "20% – 30%", color: "bg-[#707881]", matchBadge: "Low/Possible", badgeColor: "text-[#707881]", support: "Supporting: Pruritic throat, absence of wheezing, non-purulent drainage." },
    { rank: 4, name: "Acute Bronchitis (Early Stage)", icd: "ICD-10: J20.9", prob: 14, range: "10% – 18%", color: "bg-[#bfc7d2]", matchBadge: "Marginal Probability", badgeColor: "text-[#707881]", support: "Substernal tightness noted; low incidence of deep bronchial rhonchi." },
  ];

  return (
    <section className="xl:col-span-7 flex flex-col gap-6">
      {/* Top Diagnostic Metric Overview Bar */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div className="bg-white p-5 rounded-2xl shadow-sm border border-[#dae2fd] flex flex-col justify-between">
          <div className="flex items-center justify-between text-[#3f4850]">
            <span className="text-xs uppercase tracking-wider font-bold">Triage Confidence</span>
            <span className="material-symbols-outlined text-[24px] text-[#006194]">insights</span>
          </div>
          <div className="my-2.5 flex items-baseline gap-2.5">
            <span className="text-4xl font-extrabold text-[#006194]">
              {triageData?.confidence ? `${triageData.confidence}%` : '94.2%'}
            </span>
            <span className="text-xs font-mono text-[#006c49] flex items-center font-bold">
              <span className="material-symbols-outlined text-[16px]">trending_up</span> +3.1%
            </span>
          </div>
          <p className="text-xs text-[#3f4850]">Bayesian multi-factor convergence score</p>
        </div>

        <div className="bg-white p-5 rounded-2xl shadow-sm border border-[#dae2fd] flex flex-col justify-between">
          <div className="flex items-center justify-between text-[#3f4850]">
            <span className="text-xs uppercase tracking-wider font-bold">Respiratory Acuity</span>
            <span className="material-symbols-outlined text-[24px] text-amber-600">pulmonology</span>
          </div>
          <div className="my-2.5 flex items-baseline gap-2.5">
            <span className="text-4xl font-extrabold text-amber-600">Grade II</span>
            <span className="text-xs font-bold text-amber-800 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
              Mild/Exertional
            </span>
          </div>
          <p className="text-xs text-[#3f4850]">No stridor or accessory muscle usage reported</p>
        </div>

        <div className="bg-white p-5 rounded-2xl shadow-sm border border-[#dae2fd] flex flex-col justify-between">
          <div className="flex items-center justify-between text-[#3f4850]">
            <span className="text-xs uppercase tracking-wider font-bold">Telemetry Stability</span>
            <span className="material-symbols-outlined text-[24px] text-[#006c49]">monitor_heart</span>
          </div>
          <div className="my-2.5 flex items-baseline gap-2.5">
            <span className="text-4xl font-extrabold text-[#006c49]">Optimal</span>
            <span className="text-xs font-bold text-[#006c49] bg-[#6cf8bb]/30 px-2 py-0.5 rounded">
              Normotensive
            </span>
          </div>
          <p className="text-xs text-[#3f4850]">Resting HR 82 bpm • Temp stable at 100.4°F</p>
        </div>
      </div>

      {/* Main Differential Diagnosis Spectrum Card */}
      <div className="bg-white p-6 sm:p-7 rounded-2xl shadow-sm border border-[#dae2fd] flex flex-col gap-5">
        <div className="flex items-center justify-between flex-wrap gap-2">
          <div>
            <div className="flex items-center gap-2.5">
              <span className="w-3 h-3 rounded-full bg-[#006194]"></span>
              <h2 className="text-lg font-bold text-[#131b2e]">Differential Diagnosis Ranking & Probabilities</h2>
            </div>
            <p className="text-xs sm:text-sm text-[#3f4850] mt-0.5">
              Ranked clinical matches weighted against ICD-10 criteria and real-time patient telemetry
            </p>
          </div>

          <div className="flex items-center gap-2">
            <span className="px-2.5 py-1 rounded-lg bg-[#eaedff] text-xs font-mono text-[#00628d] font-bold">
              CI: 95% Interval
            </span>
            <button
              onClick={() => alert("Filter applied.")}
              className="px-3 py-1 rounded-lg bg-[#f2f3ff] hover:bg-[#eaedff] text-[#3f4850] text-xs font-semibold transition-colors"
            >
              Filter Specialty
            </button>
          </div>
        </div>

        {/* Probability Progress Rows */}
        <div className="flex flex-col gap-3.5 mt-1">
          {topMatches.map((m) => (
            <div
              key={m.rank}
              className="flex flex-col gap-1.5 p-3.5 sm:p-4 rounded-xl bg-[#f2f3ff]/70 hover:bg-[#f2f3ff] transition-colors border border-[#dae2fd]/60"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5 flex-wrap">
                  <span className="w-6 h-6 rounded-lg bg-[#cce5ff] text-[#004b73] flex items-center justify-center text-xs font-mono font-extrabold">
                    {m.rank}
                  </span>
                  <span className="text-sm sm:text-base font-bold text-[#131b2e]">{m.name}</span>
                  <span className="px-2 py-0.5 rounded bg-[#eaedff] text-xs font-mono text-[#3f4850] font-semibold">
                    {m.icd}
                  </span>
                </div>
                <div className="flex items-center gap-3 font-mono">
                  <span className="text-xs text-[#3f4850] hidden sm:inline">{m.range}</span>
                  <span className="text-lg font-black text-[#006194]">{m.prob}%</span>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="w-full h-3 bg-[#eaedff] rounded-full overflow-hidden relative mt-1">
                <div
                  className={`h-full ${m.color} rounded-full transition-all duration-700 ease-out`}
                  style={{ width: `${m.prob}%` }}
                />
              </div>

              <div className="flex items-center justify-between text-[#3f4850] text-xs font-mono mt-0.5">
                <span>{m.support}</span>
                <span className={`font-bold ${m.badgeColor}`}>{m.matchBadge}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Bento Grid Split: Radar Chart & Normal Distribution Curve */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Symptom Cluster Intensity Radar */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-[#dae2fd] flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-base font-bold text-[#131b2e]">Cluster Intensity Radar</h3>
              <p className="text-xs text-[#3f4850]">Multi-axial clinical load profile</p>
            </div>
            <span className="px-2.5 py-0.5 rounded-full bg-[#6cf8bb]/30 text-[#006c49] text-xs font-mono font-bold">
              Calibrated
            </span>
          </div>

          {/* Radar SVG Visualization */}
          <div className="w-full flex items-center justify-center py-5">
            <svg className="w-68 h-68 sm:w-76 sm:h-76 overflow-visible" viewBox="0 0 240 240">
              <polygon className="text-[#dae2fd]" fill="none" points="120,40 190,120 120,200 50,120" stroke="currentColor" strokeDasharray="3 3" strokeWidth="1.5" />
              <polygon className="text-[#dae2fd]" fill="none" points="120,65 165,120 120,175 75,120" stroke="currentColor" strokeWidth="1.5" />
              <polygon className="text-[#dae2fd]" fill="none" points="120,90 145,120 120,150 95,120" stroke="currentColor" strokeWidth="1.5" />

              <line className="text-[#bfc7d2]/70" stroke="currentColor" strokeWidth="1" x1="120" x2="120" y1="25" y2="215" />
              <line className="text-[#bfc7d2]/70" stroke="currentColor" strokeWidth="1" x1="25" x2="215" y1="120" y2="120" />

              <polygon className="transition-all duration-500" fill="rgba(0, 97, 148, 0.25)" points="120,37 144,120 120,176 84,120" stroke="#006194" strokeWidth="2.8" />

              <circle className="ring-4 ring-[#cce5ff]" cx="120" cy="37" fill="#006194" r="5" />
              <circle cx="144" cy="120" fill="#006194" r="4.5" />
              <circle cx="120" cy="176" fill="#006194" r="4.5" />
              <circle cx="84" cy="120" fill="#006194" r="4.5" />

              <text className="fill-[#131b2e] text-[11px] font-extrabold" textAnchor="middle" x="120" y="16">RESPIRATORY (85%)</text>
              <text className="fill-[#131b2e] text-[11px] font-extrabold" textAnchor="start" x="210" y="124">PAIN (30%)</text>
              <text className="fill-[#131b2e] text-[11px] font-extrabold" textAnchor="middle" x="120" y="234">SYSTEMIC (70%)</text>
              <text className="fill-[#131b2e] text-[11px] font-extrabold" textAnchor="end" x="30" y="124">FATIGUE (45%)</text>
            </svg>
          </div>

          <div className="grid grid-cols-2 gap-3 text-center border-t border-[#eaedff] pt-3.5">
            <div className="bg-[#f2f3ff] p-2.5 rounded-xl">
              <span className="text-xs text-[#3f4850] block font-mono">Primary Driver</span>
              <span className="text-xs sm:text-sm text-[#006194] font-bold">Bronchial Sensitivity</span>
            </div>
            <div className="bg-[#f2f3ff] p-2.5 rounded-xl">
              <span className="text-xs text-[#3f4850] block font-mono">Alleviating Factor</span>
              <span className="text-xs sm:text-sm text-[#006c49] font-bold">No Neuralgia</span>
            </div>
          </div>
        </div>

        {/* Demographic Baseline Risk Distribution Curve */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-[#dae2fd] flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-base font-bold text-[#131b2e]">Demographic Risk Curve</h3>
              <p className="text-xs text-[#3f4850]">Cohort: Female, Age 30–35, Non-smoker</p>
            </div>
            <span className="px-2.5 py-0.5 rounded bg-[#eaedff] text-xs font-mono text-[#131b2e] font-bold">
              n = 142,800
            </span>
          </div>

          {/* Normal Distribution Bell Curve SVG */}
          <div className="w-full flex flex-col items-center justify-center py-5">
            <svg className="w-full h-48 sm:h-52 overflow-visible" viewBox="0 0 320 140">
              <defs>
                <linearGradient id="bellGradient" x1="0%" x2="0%" y1="0%" y2="100%">
                  <stop offset="0%" stopColor="#006194" stopOpacity="0.35" />
                  <stop offset="100%" stopColor="#006194" stopOpacity="0.0" />
                </linearGradient>
              </defs>

              <line className="text-[#dae2fd]" stroke="currentColor" strokeWidth="2" x1="20" x2="300" y1="120" y2="120" />

              <path d="M 20 120 C 70 120, 100 115, 120 70 C 140 25, 160 15, 160 15 C 160 15, 180 25, 200 70 C 220 115, 250 120, 300 120 Z" fill="url(#bellGradient)" />
              <path d="M 20 120 C 70 120, 100 115, 120 70 C 140 25, 160 15, 160 15 C 160 15, 180 25, 200 70 C 220 115, 250 120, 300 120" fill="none" stroke="#00628d" strokeWidth="2.8" />

              <line stroke="#ba1a1a" strokeDasharray="3 3" strokeWidth="2.2" x1="188" x2="188" y1="20" y2="120" />
              <circle className="animate-ping opacity-75" cx="188" cy="52" fill="#ba1a1a" r="5.5" />
              <circle cx="188" cy="52" fill="#ba1a1a" r="4.5" />

              <text className="fill-[#ba1a1a] text-[11px] font-bold" textAnchor="middle" x="188" y="14">Patient (68th %ile)</text>
              <text className="fill-[#3f4850] text-[11px] font-semibold" textAnchor="middle" x="160" y="135">μ (Mean)</text>
              <text className="fill-[#3f4850] text-[11px] font-semibold" textAnchor="middle" x="90" y="135">-1σ</text>
              <text className="fill-[#3f4850] text-[11px] font-semibold" textAnchor="middle" x="230" y="135">+1σ</text>
            </svg>
          </div>

          <div className="bg-[#f2f3ff] p-3 rounded-xl flex items-center justify-between text-[#3f4850] text-xs font-mono">
            <span className="flex items-center gap-1.5 text-[#131b2e] font-medium">
              <span className="material-symbols-outlined text-[18px] text-amber-600">tune</span> 
              Symptom severity is slightly elevated (+0.47 SD) compared to peer cohort.
            </span>
            <span className="font-bold text-[#006194]">Normal range: &lt; 85th</span>
          </div>
        </div>
      </div>

      {/* Doctor-Ready Diagnostic Export Card */}
      <div className="bg-gradient-to-br from-[#cce5ff]/50 via-white to-white p-6 sm:p-7 rounded-2xl shadow-sm border border-[#dae2fd] flex flex-col md:flex-row items-start md:items-center justify-between gap-5">
        <div className="flex items-start gap-4">
          <div className="w-14 h-14 rounded-2xl bg-[#006194] text-white flex items-center justify-center shrink-0 shadow-sm">
            <span className="material-symbols-outlined text-[30px]">assignment_turned_in</span>
          </div>
          <div>
            <div className="flex items-center gap-2.5">
              <h3 className="text-base sm:text-lg font-bold text-[#131b2e]">Doctor-Ready Diagnostic Summary</h3>
              <span className="px-2.5 py-0.5 rounded-full bg-[#006c49] text-white text-xs font-bold">
                Pro Feature
              </span>
            </div>
            <p className="text-xs sm:text-sm text-[#3f4850] mt-1 max-w-2xl leading-relaxed">
              Includes SBAR formatted clinical handoff, time-series vitals chart, ICD-10 suggestions, and cryptographic hash verification for direct EHR ingestion.
            </p>
            <div className="flex items-center gap-3 mt-2 text-xs font-mono text-[#707881]">
              <span>Generated: Today at 09:44:12</span>
              <span>•</span>
              <span>Format: PDF / HL7 FHIR Bundle</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3 shrink-0 w-full md:w-auto">
          <button
            onClick={onDownloadPDF}
            className="flex-1 md:flex-initial px-5 py-3 rounded-xl bg-[#006194] hover:bg-[#007bb9] text-white text-xs sm:text-sm font-bold transition-all shadow-md shadow-[#006194]/20 flex items-center justify-center gap-2 active:scale-95"
          >
            <span className="material-symbols-outlined text-[20px]">download</span>
            <span>Download Summary PDF</span>
          </button>
          <button
            onClick={onOpenSummaryModal}
            className="px-4 py-3 rounded-xl bg-white hover:bg-[#eaedff] text-[#131b2e] border border-[#dae2fd] transition-colors shadow-sm flex items-center justify-center active:scale-95"
            title="Preview SBAR Report"
          >
            <span className="material-symbols-outlined text-[20px]">visibility</span>
          </button>
        </div>
      </div>
    </section>
  );
}
