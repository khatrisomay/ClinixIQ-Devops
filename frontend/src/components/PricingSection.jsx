import React from 'react';

export default function PricingSection({ onUpgradePro, onScheduleB2B }) {
  return (
    <section className="w-full px-4 sm:px-8 lg:px-12 py-14" id="pricingSection">
      <div className="w-full flex flex-col items-center">
        {/* Section Title & Narrative */}
        <div className="text-center max-w-4xl mb-10">
          <span className="px-3.5 py-1.5 rounded-full bg-[#cce5ff] text-[#004b73] text-xs font-bold uppercase tracking-wider font-mono">
            Clinical Licensing & Tiers
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-[#131b2e] mt-3 tracking-tight">
            Designed for Patients, Clinicians & Health Systems
          </h2>
          <p className="text-base sm:text-lg text-[#3f4850] mt-2.5 leading-relaxed">
            Choose calibrated clinical intelligence. Upgrade anytime to access longitudinal biometrics and doctor-ready clinical handoffs.
          </p>
        </div>

        {/* Pricing Matrix Bento Cards */}
        <div className="w-full grid grid-cols-1 lg:grid-cols-3 gap-8 items-stretch">
          {/* Tier 1: Free Tier */}
          <div className="bg-white rounded-2xl p-7 sm:p-8 shadow-sm border border-[#dae2fd] flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between">
                <span className="text-base font-bold text-[#3f4850]">Standard Care</span>
                <span className="px-2.5 py-1 rounded bg-[#eaedff] text-[#131b2e] text-xs font-mono font-bold">Individual</span>
              </div>
              <div className="mt-5 flex items-baseline gap-1.5">
                <span className="text-4xl sm:text-5xl font-extrabold text-[#131b2e]">$0</span>
                <span className="text-sm text-[#3f4850]">/ month</span>
              </div>
              <p className="text-sm text-[#3f4850] mt-2.5 leading-relaxed">Essential AI diagnostic guidance for mild sporadic acute symptoms.</p>
              <div className="w-full h-[1px] bg-[#eaedff] my-6"></div>
              <ul className="flex flex-col gap-3.5 text-sm text-[#131b2e]">
                <li className="flex items-center gap-2.5">
                  <span className="material-symbols-outlined text-[20px] text-[#006c49]">check_circle</span>
                  <span>3 Triage evaluations / month</span>
                </li>
                <li className="flex items-center gap-2.5">
                  <span className="material-symbols-outlined text-[20px] text-[#006c49]">check_circle</span>
                  <span>Standard probabilistic differential matching</span>
                </li>
                <li className="flex items-center gap-2.5">
                  <span className="material-symbols-outlined text-[20px] text-[#006c49]">check_circle</span>
                  <span>Basic home self-care recommendations</span>
                </li>
                <li className="flex items-center gap-2.5 text-[#707881]">
                  <span className="material-symbols-outlined text-[20px]">cancel</span>
                  <span>EHR-compatible summary exports</span>
                </li>
                <li className="flex items-center gap-2.5 text-[#707881]">
                  <span className="material-symbols-outlined text-[20px]">cancel</span>
                  <span>Longitudinal telemetry history</span>
                </li>
              </ul>
            </div>
            <div className="mt-10">
              <button
                type="button"
                className="w-full py-3.5 rounded-xl bg-[#e2e7ff] text-[#131b2e] text-sm font-bold transition-colors cursor-default"
              >
                Current Active Plan
              </button>
            </div>
          </div>

          {/* Tier 2: Pro Tier (Highlighted / Most Popular) */}
          <div className="bg-white rounded-2xl p-7 sm:p-8 shadow-xl border-2 border-[#006194] relative flex flex-col justify-between transform lg:-translate-y-2">
            <div className="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1.5 rounded-full bg-[#006194] text-white text-xs font-bold shadow-md tracking-wide uppercase">
              Most Popular
            </div>
            <div>
              <div className="flex items-center justify-between">
                <span className="text-base font-bold text-[#006194]">ClinixIQ Pro</span>
                <span className="px-2.5 py-1 rounded bg-[#cce5ff] text-[#004b73] text-xs font-mono font-bold">
                  Full Diagnostic Suite
                </span>
              </div>
              <div className="mt-5 flex items-baseline gap-1.5">
                <span className="text-4xl sm:text-5xl font-extrabold text-[#006194]">$9.99</span>
                <span className="text-sm text-[#3f4850]">/ month</span>
              </div>
              <p className="text-sm text-[#3f4850] mt-2.5 leading-relaxed">
                Uncompromised clinical acuity support, longitudinal health vaults, and rapid doctor-ready handoffs.
              </p>
              <div className="w-full h-[1px] bg-[#cce5ff] my-6"></div>
              <ul className="flex flex-col gap-3.5 text-sm text-[#131b2e]">
                <li className="flex items-center gap-2.5 font-medium">
                  <span className="material-symbols-outlined text-[20px] text-[#006194]" style={{ fontVariationSettings: "'FILL' 1" }}>
                    check_circle
                  </span>
                  <span><strong>Unlimited</strong> AI clinical assessments</span>
                </li>
                <li className="flex items-center gap-2.5">
                  <span className="material-symbols-outlined text-[20px] text-[#006194]" style={{ fontVariationSettings: "'FILL' 1" }}>
                    check_circle
                  </span>
                  <span>Longitudinal symptom tracking & radar trends</span>
                </li>
                <li className="flex items-center gap-2.5 font-medium">
                  <span className="material-symbols-outlined text-[20px] text-[#006194]" style={{ fontVariationSettings: "'FILL' 1" }}>
                    check_circle
                  </span>
                  <span>Doctor-ready exportable clinical PDFs & SBAR summaries</span>
                </li>
                <li className="flex items-center gap-2.5">
                  <span className="material-symbols-outlined text-[20px] text-[#006194]" style={{ fontVariationSettings: "'FILL' 1" }}>
                    check_circle
                  </span>
                  <span>Priority urgent care & telehealth queue integration</span>
                </li>
                <li className="flex items-center gap-2.5">
                  <span className="material-symbols-outlined text-[20px] text-[#006194]" style={{ fontVariationSettings: "'FILL' 1" }}>
                    check_circle
                  </span>
                  <span>Family profile management (up to 4 members)</span>
                </li>
              </ul>
            </div>
            <div className="mt-10">
              <button
                type="button"
                onClick={onUpgradePro}
                className="w-full py-3.5 rounded-xl bg-[#006194] hover:bg-[#007bb9] text-white text-sm font-bold transition-all shadow-md shadow-[#006194]/25 active:scale-95"
              >
                Upgrade to ClinixIQ Pro
              </button>
              <p className="text-center text-xs font-mono text-[#3f4850] mt-2.5">Cancel anytime • 14-day clinical guarantee</p>
            </div>
          </div>

          {/* Tier 3: B2B Enterprise / White-Label Card */}
          <div className="bg-white rounded-2xl p-7 sm:p-8 shadow-sm border border-[#dae2fd] flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between">
                <span className="text-base font-bold text-[#3f4850]">Institutional / B2B</span>
                <span className="px-2.5 py-1 rounded bg-[#eaedff] text-[#131b2e] text-xs font-mono font-bold">
                  Health Systems
                </span>
              </div>
              <div className="mt-5 flex items-baseline gap-1.5">
                <span className="text-3xl sm:text-4xl font-extrabold text-[#131b2e]">Custom</span>
                <span className="text-sm text-[#3f4850]">/ volume tier</span>
              </div>
              <p className="text-sm text-[#3f4850] mt-2.5 leading-relaxed">For ambulatory networks, telehealth providers, and hospital triage dispatchers.</p>
              <div className="w-full h-[1px] bg-[#eaedff] my-6"></div>
              <ul className="flex flex-col gap-3.5 text-sm text-[#131b2e]">
                <li className="flex items-center gap-2.5">
                  <span className="material-symbols-outlined text-[20px] text-[#006c49]">check_circle</span>
                  <span>Direct EHR Integration (Epic & Cerner FHIR API)</span>
                </li>
                <li className="flex items-center gap-2.5">
                  <span className="material-symbols-outlined text-[20px] text-[#006c49]">check_circle</span>
                  <span>Custom hospital clinical pathways & protocols</span>
                </li>
                <li className="flex items-center gap-2.5">
                  <span className="material-symbols-outlined text-[20px] text-[#006c49]">check_circle</span>
                  <span>Enterprise BAA, dedicated SLA & SSO security</span>
                </li>
                <li className="flex items-center gap-2.5">
                  <span className="material-symbols-outlined text-[20px] text-[#006c49]">check_circle</span>
                  <span>White-label patient portal embed</span>
                </li>
              </ul>
            </div>
            <div className="mt-10">
              <button
                type="button"
                onClick={onScheduleB2B}
                className="w-full py-3.5 rounded-xl bg-[#eaedff] hover:bg-[#dae2fd] text-[#131b2e] text-sm font-bold transition-colors active:scale-95"
              >
                Schedule Enterprise Briefing
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
