import React, { useEffect, useState } from 'react';
import { CheckCircle2, XCircle, Sparkles, ArrowRight, X } from 'lucide-react';

export default function CheckoutFeedbackModal({ onPlanUpdated }) {
  const [feedbackState, setFeedbackState] = useState(null); // 'success' | 'canceled' | null
  const [sessionId, setSessionId] = useState(null);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const status = params.get('status');
    const sessId = params.get('session_id');
    const canceled = params.get('canceled');

    if (status === 'success' && sessId) {
      setFeedbackState('success');
      setSessionId(sessId);
      if (onPlanUpdated) {
        onPlanUpdated('pro');
      }
      // Clean up URL without page reload
      window.history.replaceState({}, document.title, window.location.pathname);
    } else if (canceled === 'true') {
      setFeedbackState('canceled');
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, [onPlanUpdated]);

  if (!feedbackState) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-white dark:bg-slate-900 rounded-3xl max-w-md w-full border border-slate-200 dark:border-slate-800 shadow-2xl overflow-hidden p-6 sm:p-8 text-center space-y-6">
        {feedbackState === 'success' ? (
          <>
            <div className="w-16 h-16 mx-auto rounded-full bg-emerald-100 dark:bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 flex items-center justify-center shadow-lg shadow-emerald-500/10">
              <CheckCircle2 className="w-9 h-9" />
            </div>

            <div className="space-y-2">
              <span className="text-xs font-bold uppercase tracking-wider text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-200 dark:border-emerald-500/20">
                Payment Confirmed
              </span>
              <h3 className="text-2xl font-extrabold text-slate-900 dark:text-white">
                Welcome to ClinixIQ Pro!
              </h3>
              <p className="text-sm text-slate-600 dark:text-slate-400">
                Your subscription has been verified. You now have unlimited AI symptom triage, longitudinal analytics, and instant EHR-compatible doctor exports.
              </p>
              {sessionId && (
                <p className="text-[11px] font-mono text-slate-400 pt-1">
                  Session: {sessionId.slice(0, 20)}...
                </p>
              )}
            </div>

            <button
              type="button"
              onClick={() => setFeedbackState(null)}
              className="w-full py-3.5 px-4 rounded-xl bg-sky-500 hover:bg-sky-400 text-white font-semibold text-sm flex items-center justify-center gap-2 transition-all shadow-lg shadow-sky-500/25"
            >
              <span>Explore Pro Clinical Features</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </>
        ) : (
          <>
            <div className="w-16 h-16 mx-auto rounded-full bg-amber-100 dark:bg-amber-500/20 text-amber-600 dark:text-amber-400 flex items-center justify-center">
              <XCircle className="w-9 h-9" />
            </div>

            <div className="space-y-2">
              <h3 className="text-2xl font-extrabold text-slate-900 dark:text-white">
                Checkout Incomplete
              </h3>
              <p className="text-sm text-slate-600 dark:text-slate-400">
                Your checkout session was canceled and no charge was incurred. You can upgrade anytime to access premium clinical triage features.
              </p>
            </div>

            <button
              type="button"
              onClick={() => setFeedbackState(null)}
              className="w-full py-3 px-4 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 font-semibold text-sm transition-all"
            >
              Return to Triage Assistant
            </button>
          </>
        )}
      </div>
    </div>
  );
}
