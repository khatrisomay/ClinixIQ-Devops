import React, { useState } from 'react';
import { Check, Sparkles, Building2, Shield, Zap, ArrowRight } from 'lucide-react';

export default function PricingModal({ onSelectPlan }) {
  const [billingCycle, setBillingCycle] = useState('monthly');

  const plans = [
    {
      name: "Starter Triage",
      price: "$0",
      period: "forever free",
      desc: "Essential AI symptom triage for individuals and families.",
      features: [
        "5 AI symptom assessments / month",
        "Top 3 differential diagnoses",
        "Standard home-care triage guidance",
        "Community support"
      ],
      cta: "Current Plan",
      featured: false,
    },
    {
      name: "Pro Patient & Care",
      price: billingCycle === 'monthly' ? "$9.99" : "$7.99",
      period: "per month",
      desc: "Comprehensive health monitoring and clinician-ready reports.",
      features: [
        "Unlimited AI triage queries",
        "Exportable PDF doctor summaries",
        "Python biomarker & risk trend curves",
        "Priority ML inference queue (<50ms)",
        "Chronic symptom tracking calendar"
      ],
      cta: "Upgrade to Pro",
      featured: true,
      popularBadge: "Most Popular",
    },
    {
      name: "Clinic / Telehealth API",
      price: billingCycle === 'monthly' ? "$149" : "$119",
      period: "per month",
      desc: "Commercial API access for telehealth apps and private clinics.",
      features: [
        "10,000 API triage evaluations / month",
        "Dedicated Kubernetes ingress endpoint",
        "HIPAA-aligned anonymization pipeline",
        "Custom disease probability weighting",
        "99.9% uptime SLA & priority engineer support"
      ],
      cta: "Contact Enterprise",
      featured: false,
    }
  ];

  return (
    <div className="max-w-6xl mx-auto py-4 sm:py-8 space-y-10">
      {/* Header */}
      <div className="text-center space-y-3 max-w-2xl mx-auto">
        <span className="text-xs font-bold uppercase tracking-wider text-sky-400 bg-sky-500/10 px-3 py-1 rounded-full border border-sky-500/20">
          Commercial SaaS Plans
        </span>
        <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          Transparent Pricing for Patients, Doctors & Clinics
        </h2>
        <p className="text-slate-400 text-sm">
          Select an individual plan for personal diagnostic tracking or integrate our Kubernetes-powered ML microservices into your clinic.
        </p>

        {/* Billing Toggle */}
        <div className="pt-2 flex items-center justify-center space-x-3 text-xs font-semibold">
          <span className={billingCycle === 'monthly' ? 'text-white' : 'text-slate-500'}>Monthly</span>
          <button
            onClick={() => setBillingCycle(billingCycle === 'monthly' ? 'annual' : 'monthly')}
            className="w-12 h-6 bg-slate-800 rounded-full p-1 border border-slate-700 flex items-center transition-all"
          >
            <div
              className={`w-4 h-4 rounded-full bg-sky-400 transition-transform ${
                billingCycle === 'annual' ? 'translate-x-6' : 'translate-x-0'
              }`}
            />
          </button>
          <span className={billingCycle === 'annual' ? 'text-white' : 'text-slate-500'}>
            Annual <span className="text-emerald-400 text-[10px] bg-emerald-500/10 px-1.5 py-0.5 rounded border border-emerald-500/20">Save 20%</span>
          </span>
        </div>
      </div>

      {/* Plan Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-stretch">
        {plans.map((plan, idx) => (
          <div
            key={idx}
            className={`rounded-2xl p-6 sm:p-8 relative flex flex-col justify-between transition-all duration-300 ${
              plan.featured
                ? 'bg-gradient-to-b from-sky-950/80 via-slate-900 to-slate-900 border-2 border-sky-500 shadow-2xl shadow-sky-500/20 md:-translate-y-2'
                : 'bg-slate-900/90 border border-slate-800 hover:border-slate-700'
            }`}
          >
            {plan.popularBadge && (
              <span className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 bg-gradient-to-r from-sky-500 to-blue-600 text-white text-[11px] font-bold rounded-full uppercase tracking-wider shadow-md">
                {plan.popularBadge}
              </span>
            )}

            <div>
              <h3 className="text-xl font-bold text-white">{plan.name}</h3>
              <p className="text-xs text-slate-400 mt-1 min-h-[32px]">{plan.desc}</p>

              <div className="my-6">
                <span className="text-4xl font-extrabold text-white">{plan.price}</span>
                <span className="text-xs text-slate-400 ml-2 font-medium">{plan.period}</span>
              </div>

              <div className="border-t border-slate-800/80 pt-6 mb-8">
                <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-3">Included Capabilities:</div>
                <ul className="space-y-3 text-xs text-slate-300">
                  {plan.features.map((feat, fIdx) => (
                    <li key={fIdx} className="flex items-start space-x-2.5">
                      <Check className="w-4 h-4 text-sky-400 shrink-0 mt-0.5" />
                      <span>{feat}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            <button
              onClick={() => onSelectPlan && onSelectPlan(plan.name)}
              className={`w-full py-3 text-xs font-bold rounded-xl transition-all flex items-center justify-center space-x-2 shadow-md ${
                plan.featured
                  ? 'bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-400 hover:to-blue-500 text-white shadow-sky-500/25 active:scale-95'
                  : 'bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 active:scale-95'
              }`}
            >
              <span>{plan.cta}</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        ))}
      </div>

      {/* Enterprise Assurance Banner */}
      <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-400">
        <div className="flex items-center space-x-3">
          <Shield className="w-5 h-5 text-emerald-400 shrink-0" />
          <span>Need custom Kubernetes namespace deployment, on-premise model weights, or BAA for HIPAA compliance?</span>
        </div>
        <button className="text-sky-400 hover:text-sky-300 font-semibold whitespace-nowrap">
          Schedule Clinical Architecture Review &rarr;
        </button>
      </div>
    </div>
  );
}
