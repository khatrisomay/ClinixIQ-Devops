import React, { useState, useEffect } from 'react';
import { Shield, Sparkles, CheckCircle, ExternalLink, RefreshCw, X, CreditCard } from 'lucide-react';
import { fetchSubscription, fetchUsage, openCustomerPortal } from '../services/billing';

export default function SubscriptionStatusModal({ isOpen, onClose, customerId = 'patient_demo', currentTier = 'starter', onUpgradeClick }) {
  const [subData, setSubData] = useState(null);
  const [usageData, setUsageData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpeningPortal, setIsOpeningPortal] = useState(false);

  useEffect(() => {
    if (isOpen) {
      loadData();
    }
  }, [isOpen, customerId]);

  const loadData = async () => {
    setIsLoading(true);
    try {
      const [sub, usage] = await Promise.all([
        fetchSubscription(customerId).catch(() => null),
        fetchUsage(customerId).catch(() => null),
      ]);
      setSubData(sub);
      setUsageData(usage);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  const handleOpenStripePortal = async () => {
    setIsOpeningPortal(true);
    try {
      const resp = await openCustomerPortal(customerId);
      if (resp.portal_url) {
        window.location.href = resp.portal_url;
      }
    } catch (e) {
      alert(e.message || 'Failed to open Stripe billing portal');
    } finally {
      setIsOpeningPortal(false);
    }
  };

  if (!isOpen) return null;

  const tier = subData?.plan_tier || currentTier;
  const isPro = tier === 'pro';
  const isEnterprise = tier === 'enterprise';
  const usedCount = usageData?.triage_evaluations_used || 0;
  const quotaLimit = usageData?.quota_limit ?? (isPro ? -1 : 5);
  const isUnlimited = quotaLimit === -1;
  const percentUsed = isUnlimited ? 15 : Math.min(100, Math.round((usedCount / quotaLimit) * 100));

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-white dark:bg-slate-900 rounded-3xl max-w-lg w-full border border-slate-200 dark:border-slate-800 shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="p-6 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className={`p-2.5 rounded-2xl ${
              isPro ? 'bg-sky-500/10 text-sky-500' : isEnterprise ? 'bg-indigo-500/10 text-indigo-500' : 'bg-slate-100 dark:bg-slate-800 text-slate-600'
            }`}>
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-bold text-slate-900 dark:text-white text-lg">
                Subscription & Quota
              </h3>
              <p className="text-xs text-slate-500">Managed via Stripe Billing API</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        <div className="p-6 space-y-6">
          {/* Current Tier Badge Card */}
          <div className="p-5 rounded-2xl bg-gradient-to-r from-sky-500/10 to-indigo-500/10 border border-sky-500/20 flex items-center justify-between">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-sky-600 dark:text-sky-400">
                Active Tier
              </span>
              <div className="text-2xl font-extrabold text-slate-900 dark:text-white capitalize mt-0.5">
                {tier} Plan
              </div>
              <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-emerald-600 dark:text-emerald-400 mt-1">
                <CheckCircle className="w-3.5 h-3.5" />
                Active Subscription
              </span>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-slate-900 dark:text-white">
                {isPro ? '$9.99/mo' : isEnterprise ? '$149.00/mo' : '$0.00'}
              </span>
              <p className="text-xs text-slate-400">
                {subData?.billing_cycle === 'annual' ? 'Annual Cycle' : 'Monthly Cycle'}
              </p>
            </div>
          </div>

          {/* Monthly Quota Consumption */}
          <div className="space-y-2.5">
            <div className="flex items-center justify-between text-sm">
              <span className="font-semibold text-slate-700 dark:text-slate-300">
                Monthly Triage Usage
              </span>
              <span className="font-bold text-slate-900 dark:text-white font-mono text-xs">
                {isUnlimited ? `${usedCount} / Unlimited` : `${usedCount} / ${quotaLimit} Queries`}
              </span>
            </div>
            <div className="w-full h-3 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden p-0.5">
              <div
                className={`h-full rounded-full transition-all duration-500 ${
                  percentUsed >= 90
                    ? 'bg-rose-500'
                    : isPro
                    ? 'bg-gradient-to-r from-sky-500 to-indigo-500'
                    : 'bg-sky-500'
                }`}
                style={{ width: `${isUnlimited ? 100 : percentUsed}%` }}
              />
            </div>
            <p className="text-xs text-slate-500">
              {isUnlimited
                ? 'High-priority ML inference queue active.'
                : `${Math.max(0, quotaLimit - usedCount)} queries remaining in current monthly cycle.`}
            </p>
          </div>

          {/* Action Buttons */}
          <div className="pt-2 flex flex-col sm:flex-row gap-3">
            <button
              onClick={handleOpenStripePortal}
              disabled={isOpeningPortal}
              className="flex-1 py-3 px-4 rounded-xl bg-slate-900 dark:bg-white text-white dark:text-slate-900 font-semibold text-sm hover:bg-slate-800 dark:hover:bg-slate-100 flex items-center justify-center gap-2 transition-all shadow-md"
            >
              <CreditCard className="w-4 h-4" />
              <span>{isOpeningPortal ? 'Connecting...' : 'Manage via Stripe'}</span>
              <ExternalLink className="w-3.5 h-3.5 opacity-60" />
            </button>

            {!isPro && !isEnterprise && (
              <button
                onClick={() => {
                  onClose();
                  if (onUpgradeClick) onUpgradeClick();
                }}
                className="py-3 px-4 rounded-xl bg-sky-500 hover:bg-sky-400 text-white font-semibold text-sm flex items-center justify-center gap-2 transition-all shadow-lg shadow-sky-500/25"
              >
                <Sparkles className="w-4 h-4" />
                <span>Upgrade Plan</span>
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
