import React, { useState } from 'react';
import { Check, Sparkles, Building2, Shield, Zap, ArrowRight, Loader2, AlertCircle } from 'lucide-react';
import { createCheckoutSession } from '../services/billing';

export default function PricingModal({ onSelectPlan, customerEmail = 'patient@clinixiq.health', currentTier = 'starter' }) {
  const [billingCycle, setBillingCycle] = useState('monthly');
  const [loadingTier, setLoadingTier] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  const plans = [
    {
      tier: 'starter',
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
      cta: currentTier === 'starter' ? "Current Plan" : "Downgrade",
      featured: false,
    },
    {
      tier: 'pro',
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
      cta: currentTier === 'pro' ? "Current Plan" : "Upgrade to Pro",
      featured: true,
      popularBadge: "Most Popular",
    },
    {
      tier: 'enterprise',
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
      cta: currentTier === 'enterprise' ? "Current Plan" : "Subscribe Enterprise",
      featured: false,
    }
  ];

  const handlePlanCheckout = async (plan) => {
    if (plan.tier === currentTier) return;
    setErrorMsg(null);
    setLoadingTier(plan.tier);

    try {
      const resp = await createCheckoutSession({
        customerEmail: customerEmail,
        planTier: plan.tier,
        billingCycle: billingCycle,
        customerId: `cus_${customerEmail.replace(/[^a-zA-Z0-9]/g, '_')}`,
      });

      if (resp.checkout_url) {
        window.location.href = resp.checkout_url;
      } else if (onSelectPlan) {
        onSelectPlan(plan.tier);
      }
    } catch (err) {
      console.error("Checkout error:", err);
      setErrorMsg(err.message || 'Failed to initiate Stripe checkout');
      setLoadingTier(null);
    }
  };

  return (
    <div className="max-w-6xl mx-auto py-4 sm:py-8 space-y-8">
      {/* Header */}
      <div className="text-center space-y-3 max-w-2xl mx-auto">
        <span className="text-xs font-bold uppercase tracking-wider text-sky-600 bg-sky-100 dark:bg-sky-500/10 dark:text-sky-400 px-3 py-1 rounded-full border border-sky-200 dark:border-sky-500/20">
          Commercial SaaS Plans
        </span>
        <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white tracking-tight">
          Transparent, Scalable Clinical Pricing
        </h2>
        <p className="text-slate-600 dark:text-slate-400 text-sm sm:text-base">
          From self-care acute symptom checks to enterprise health network integrations.
        </p>

        {/* Billing Cycle Toggle */}
        <div className="flex items-center justify-center gap-3 pt-4">
          <span className={`text-sm font-semibold ${billingCycle === 'monthly' ? 'text-sky-600 dark:text-sky-400' : 'text-slate-500'}`}>
            Monthly Billing
          </span>
          <button
            type="button"
            onClick={() => setBillingCycle(b => b === 'monthly' ? 'annual' : 'monthly')}
            className="relative w-14 h-7 bg-slate-200 dark:bg-slate-700 rounded-full p-1 transition-colors duration-200 ease-in-out focus:outline-none"
          >
            <div
              className={`w-5 h-5 bg-sky-500 rounded-full shadow-md transform transition-transform duration-200 ease-in-out ${
                billingCycle === 'annual' ? 'translate-x-7' : 'translate-x-0'
              }`}
            />
          </button>
          <span className={`text-sm font-semibold flex items-center gap-1.5 ${billingCycle === 'annual' ? 'text-sky-600 dark:text-sky-400' : 'text-slate-500'}`}>
            Annual Billing
            <span className="bg-emerald-100 text-emerald-700 dark:bg-emerald-500/20 dark:text-emerald-300 text-xs px-2 py-0.5 rounded-full font-bold">
              Save 20%
            </span>
          </span>
        </div>
      </div>

      {errorMsg && (
        <div className="max-w-xl mx-auto p-4 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900/50 flex items-center gap-3 text-rose-700 dark:text-rose-300 text-sm">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Pricing Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8 items-stretch">
        {plans.map((plan) => {
          const isCurrent = plan.tier === currentTier;
          const isLoading = loadingTier === plan.tier;

          return (
            <div
              key={plan.name}
              className={`relative rounded-2xl flex flex-col justify-between transition-all duration-300 ${
                plan.featured
                  ? 'bg-gradient-to-b from-sky-950/40 to-slate-900 border-2 border-sky-500 shadow-xl shadow-sky-500/10 scale-105'
                  : 'bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700'
              } p-6 sm:p-8`}
            >
              {plan.popularBadge && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-gradient-to-r from-sky-500 to-indigo-500 text-white text-xs font-bold px-3 py-1 rounded-full shadow-lg flex items-center gap-1">
                  <Sparkles className="w-3 h-3" />
                  {plan.popularBadge}
                </div>
              )}

              <div className="space-y-6">
                <div>
                  <h3 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
                    {plan.name}
                  </h3>
                  <p className="text-slate-500 dark:text-slate-400 text-xs mt-1.5 leading-relaxed">
                    {plan.desc}
                  </p>
                </div>

                <div className="flex items-baseline gap-1">
                  <span className="text-4xl font-extrabold text-slate-900 dark:text-white">
                    {plan.price}
                  </span>
                  <span className="text-slate-500 dark:text-slate-400 text-xs font-medium">
                    /{plan.period}
                  </span>
                </div>

                <div className="h-px bg-slate-200 dark:bg-slate-800" />

                <ul className="space-y-3">
                  {plan.features.map((feature, idx) => (
                    <li key={idx} className="flex items-start gap-2.5 text-xs sm:text-sm text-slate-700 dark:text-slate-300">
                      <Check className="w-4 h-4 text-sky-500 flex-shrink-0 mt-0.5" />
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="mt-8 pt-4">
                <button
                  type="button"
                  disabled={isCurrent || isLoading}
                  onClick={() => handlePlanCheckout(plan)}
                  className={`w-full py-3 px-4 rounded-xl font-semibold text-sm flex items-center justify-center gap-2 transition-all duration-200 ${
                    isCurrent
                      ? 'bg-slate-100 dark:bg-slate-800 text-slate-400 cursor-default'
                      : plan.featured
                      ? 'bg-sky-500 hover:bg-sky-400 text-white shadow-lg shadow-sky-500/25 hover:shadow-sky-500/40'
                      : 'bg-slate-900 dark:bg-white text-white dark:text-slate-900 hover:bg-slate-800 dark:hover:bg-slate-100'
                  }`}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>Redirecting to Stripe...</span>
                    </>
                  ) : (
                    <>
                      <span>{plan.cta}</span>
                      {!isCurrent && <ArrowRight className="w-4 h-4" />}
                    </>
                  )}
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
