/**
 * ClinixIQ - Commercial Billing & Stripe API Service
 */

const API_BASE = '/api/billing';

export async function fetchPlans() {
  const resp = await fetch(`${API_BASE}/plans`);
  if (!resp.ok) {
    throw new Error(`Failed to fetch pricing plans: ${resp.statusText}`);
  }
  return resp.json();
}

export async function createCheckoutSession({
  customerEmail,
  planTier,
  billingCycle = 'monthly',
  customerId = null,
  successUrl = null,
  cancelUrl = null,
}) {
  const resp = await fetch(`${API_BASE}/create-checkout-session`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      customer_email: customerEmail,
      plan_tier: planTier,
      billing_cycle: billingCycle,
      customer_id: customerId,
      success_url: successUrl,
      cancel_url: cancelUrl,
    }),
  });

  if (!resp.ok) {
    const err = await resp.json().catch(() => ({ detail: resp.statusText }));
    throw new Error(err.detail || 'Failed to initialize checkout session');
  }

  return resp.json();
}

export async function openCustomerPortal(customerId) {
  const resp = await fetch(`${API_BASE}/customer-portal`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ customer_id: customerId }),
  });

  if (!resp.ok) {
    const err = await resp.json().catch(() => ({ detail: resp.statusText }));
    throw new Error(err.detail || 'Failed to open customer portal');
  }

  return resp.json();
}

export async function fetchSubscription(customerId) {
  const resp = await fetch(`${API_BASE}/subscription/${customerId}`);
  if (!resp.ok) {
    throw new Error('Failed to load subscription details');
  }
  return resp.json();
}

export async function fetchUsage(customerId) {
  const resp = await fetch(`${API_BASE}/usage/${customerId}`);
  if (!resp.ok) {
    throw new Error('Failed to load usage record');
  }
  return resp.json();
}
